# translations/azure.py

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
        # Set default options if none are provided
        options = options or {}

        # Retrieve subscription key and region from options
        self.subscription_key = options.get('subscription_key', 'your-default-subscription-key')
        self.region = options.get('region', 'your-default-region')

        # Azure Translator endpoint
        self.endpoint = 'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0'

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
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key,
            'Ocp-Apim-Subscription-Region': self.region,
            'Content-Type': 'application/json',
        }

        # Prepare the data for Azure Translator API
        request_data = [{'Text': string.render_text()} for string in strings]

        # Define the target language for translation
        params = {'to': target_locale.language_code}

        # Make the request to the Azure Translator API
        response = requests.post(
            self.endpoint,
            headers=headers,
            params=params,
            json=request_data,
        )

        if response.status_code != 200:
            # If the API call fails, log the error and return the original strings
            print(f"Azure Translator error: {response.status_code}, {response.text}")
            return {string: string for string in strings}

        # Parse the response
        translations = response.json()

        # Create a mapping of source strings to their translations
        translated_strings = {
            string: StringValue.from_plaintext(translation['translations'][0]['text'])
            for string, translation in zip(strings, translations)
        }

        return translated_strings

    def can_translate(self, source_locale, target_locale):
        """
        Determine if translation is possible between source and target locales.

        Args:
            source_locale: Locale object for the source language.
            target_locale: Locale object for the target language.

        Returns:
            Boolean indicating if translation can occur between the locales.
        """
        # Allow translation between any different languages
        return source_locale.language_code != target_locale.language_code
