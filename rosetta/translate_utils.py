import json
import uuid

import requests

from django.conf import settings


class TranslationException(Exception):
    pass


def translate(text, from_language, to_language):
    AZURE_CLIENT_SECRET = getattr(settings, "AZURE_CLIENT_SECRET", None)
    GOOGLE_APPLICATION_CREDENTIALS_PATH = getattr(
        settings, "GOOGLE_APPLICATION_CREDENTIALS_PATH", None
    )
    GOOGLE_PROJECT_ID = getattr(settings, "GOOGLE_PROJECT_ID", None)
    DEEPL_AUTH_KEY = getattr(settings, "DEEPL_AUTH_KEY", None)
    OPENAI_API_KEY = getattr(settings, "OPENAI_API_KEY", None)

    if DEEPL_AUTH_KEY:
        deepl_language_code = None
        DEEPL_LANGUAGES = getattr(settings, "DEEPL_LANGUAGES", None)
        if type(DEEPL_LANGUAGES) is dict:
            deepl_language_code = DEEPL_LANGUAGES.get(to_language, None)

        if deepl_language_code is None:
            deepl_language_code = to_language[:2].upper()

        return translate_by_deepl(
            text,
            deepl_language_code.upper(),
            DEEPL_AUTH_KEY,
        )

    elif AZURE_CLIENT_SECRET:
        return translate_by_azure(text, from_language, to_language)

    elif GOOGLE_APPLICATION_CREDENTIALS_PATH and GOOGLE_PROJECT_ID:
        return translate_by_google(
            text,
            from_language,
            to_language,
            GOOGLE_APPLICATION_CREDENTIALS_PATH,
            GOOGLE_PROJECT_ID,
        )
    elif OPENAI_API_KEY:
        return translate_by_openai(text, from_language, to_language, OPENAI_API_KEY)
    else:
        raise TranslationException("No translation API service is configured.")


def translate_by_deepl(text, to_language, auth_key):
    if auth_key.lower().endswith(":fx"):
        endpoint = "https://api-free.deepl.com"
    else:
        endpoint = "https://api.deepl.com"

    r = requests.post(
        f"{endpoint}/v2/translate",
        headers={"Authorization": f"DeepL-Auth-Key {auth_key}"},
        data={
            "target_lang": to_language.upper(),
            "text": text,
        },
    )
    if r.status_code != 200:
        raise TranslationException(
            f"Deepl response is {r.status_code}. Please check your API key or try again later."
        )
    try:
        return r.json().get("translations")[0].get("text")
    except Exception:
        raise TranslationException("Deepl returned a non-JSON or unexpected response.")


def translate_by_azure(text, from_language, to_language):
    """
    Connects to the Azure Translator API and fetches the translation.
    :param text: The source text to be translated
    :param from_language: The language of the source text
    :param to_language: The target language to translate the text into
    :return: The translated text as a string
    """
    subscription_key = getattr(settings, "AZURE_CLIENT_SECRET", None)
    if not subscription_key:
        raise TranslationException("Azure subscription key is not configured in settings.")

    # Hardcoded region: uaenorth
    AZURE_TRANSLATOR_HOST = "https://api.cognitive.microsofttranslator.com"
    AZURE_TRANSLATOR_PATH = "/translate?api-version=3.0"

    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Ocp-Apim-Subscription-Region": "uaenorth",  # Hardcoded region
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }

    url_parameters = {"from": from_language, "to": to_language}

    request_data = [{"text": text}]

    api_hostname = AZURE_TRANSLATOR_HOST + AZURE_TRANSLATOR_PATH
    r = requests.post(
        api_hostname,
        headers=headers,
        params=url_parameters,
        json=request_data,  # Using 'json' instead of 'data' for better handling
    )
    api_response = r.json()

    try:
        # Check for errors in the API response
        if isinstance(api_response, dict) and "error" in api_response:
            api_error = api_response.get("error")
            error_code = api_error.get("code")
            error_message = api_error.get("message")

            raise TranslationException(
                f"Microsoft Translation API error: Error code {error_code}, {error_message}"
            )

        # Extract and return the translated text
        translations = api_response[0].get("translations")
        translated_text = translations[0].get("text")

        return translated_text
    except requests.exceptions.RequestException as err:
        raise TranslationException(f"Error connecting to Microsoft Translation Service: {err}")
    except Exception as e:
        raise TranslationException(f"Unexpected error: {e}")


def translate_by_google(
    text, input_language, output_language, creadentials_path, project_id
):
    from google.cloud import translate as google_translate

    client = google_translate.TranslationServiceClient.from_service_account_json(
        creadentials_path
    )
    parent = "projects/{}/locations/{}".format(project_id, "global")
    try:
        api_response = client.translate_text(
            request=dict(
                parent=parent,
                contents=[text],
                mime_type="text/plain",
                source_language_code=input_language,
                target_language_code=output_language.split(".", 1)[0],
            )
        )
    except Exception as e:
        raise TranslationException("Google API error: {}".format(e))
    else:
        return str(api_response.translations[0].translated_text)


def translate_by_openai(
    text: str, from_language: str, to_language: str, api_key: str
) -> str:
    """
    Translate text using OpenAI's GPT-3.5-turbo-instruct engine.
    param text: The text to translate.
    param from_language: The language of the text.
    param to_language: The language to translate the text into.
    param api_key: The OpenAI API key.
    return: The translated text.
    """

    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    prompt_template = getattr(
        settings,
        "OPENAI_PROMPT_TEMPLATE",
        "Translate the following text from {from_language} to {to_language}:\n\n{text}",
    )

    prompt = prompt_template.format(
        **{"from_language": from_language, "to_language": to_language, "text": text}
    )

    try:
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct", prompt=prompt
        )
        translation = response.choices[0].text.strip()
    except Exception as e:
        raise TranslationException("OpenAI API error: {}".format(e))

    return translation
