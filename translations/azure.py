import requests
from wagtail_localize.machine_translators.base import BaseMachineTranslator
from wagtail_localize.strings import StringValue

class AzureTranslator(BaseMachineTranslator):
    display_name = "Azure Translator"

    def __init__(self, options=None):
        """
        Initialize the AzureTranslator with provided configuration options.

        Args:
            options (dict): A dictionary of configuration options passed from settings.
        """
        options = options or {}
        self.subscription_key = options.get('subscription_key', 'your-default-subscription-key')
        self.region = options.get('region', 'your-default-region')
        self.endpoint = 'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0'

        # Debugging initialization
        print(f"Initialized AzureTranslator with subscription_key: {self.subscription_key}")
        print(f"Region: {self.region}")
        print(f"Endpoint: {self.endpoint}")

    def translate(self, source_locale, target_locale, strings):
        """
        Translate strings using Azure Translator.

        Args:
            source_locale: Locale object for source language.
            target_locale: Locale object for target language.
            strings: List of StringValue instances to be translated.

        Returns:
            A dictionary mapping source StringValue's to their translated values.
        """
        print(f"Translating from {source_locale.language_code} to {target_locale.language_code}")
        print(f"Strings to translate: {[string.render_text() for string in strings]}")

        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key,
            'Ocp-Apim-Subscription-Region': self.region,
            'Content-Type': 'application/json',
        }
        print(f"Request headers: {headers}")

        request_data = [{'Text': string.render_text()} for string in strings]
        print(f"Request data: {request_data}")

        params = {'to': target_locale.language_code}
        print(f"Request parameters: {params}")

        try:
            response = requests.post(
                self.endpoint,
                headers=headers,
                params=params,
                json=request_data,
            )
            print(f"Response status code: {response.status_code}")
            print(f"Response text: {response.text}")

            if response.status_code != 200:
                print(f"Error in translation: {response.status_code} - {response.text}")
                return {string: string for string in strings}

            translations = response.json()
            print(f"API translations response: {translations}")

            translated_strings = {
                string: StringValue.from_plaintext(translation['translations'][0]['text'])
                for string, translation in zip(strings, translations)
            }

            print(f"Translated strings: {translated_strings}")
            return translated_strings

        except Exception as e:
            print(f"Exception occurred: {e}")
            return {string: string for string in strings}

    def can_translate(self, source_locale, target_locale):
        """
        Determine if translation is possible between source and target locales.

        Args:
            source_locale: Locale object for the source language.
            target_locale: Locale object for the target language.

        Returns:
            Boolean indicating if translation can occur between the locales.
        """
        can_translate = source_locale.language_code != target_locale.language_code
        print(f"Can translate from {source_locale.language_code} to {target_locale.language_code}: {can_translate}")
        return can_translate
