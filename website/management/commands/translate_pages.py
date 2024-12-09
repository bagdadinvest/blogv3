from django.core.management.base import BaseCommand, CommandError
from wagtail.models import Page
from wagtail_localize.models import TranslationSource, locale
from translations.azure import AzureTranslator
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Translate Wagtail pages using Wagtail Localize and AzureTranslator.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--page-id',
            type=int,
            help='ID of the source page to translate. If omitted, all source pages will be processed.'
        )
        parser.add_argument(
            '--locales',
            nargs='+',
            help='List of target locale codes to translate into. If omitted, all non-source locales are used.'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simulate the translation process without making any changes.'
        )

    def handle(self, *args, **options):
        page_id = options.get('page_id')
        target_locales = options.get('locales')
        dry_run = options.get('dry_run')

        try:
            if page_id:
                sources = TranslationSource.objects.filter(page__id=page_id)
                if not sources.exists():
                    self.stdout.write(self.style.ERROR(f"No TranslationSource found for page ID {page_id}."))
                    return
            else:
                sources = TranslationSource.objects.all()

            # Initialize the translator
            translator = AzureTranslator()

            # Fetch all locales
            if target_locales:
                locales = Locale.objects.filter(language_code__in=target_locales)
                if not locales.exists():
                    self.stdout.write(self.style.ERROR("No matching locales found for the provided codes."))
                    return
            else:
                locales = Locale.objects.all()

            for source in sources:
                source_page = source.page
                translation_group = getattr(source_page, 'translation_group', None)

                if not translation_group:
                    self.stdout.write(self.style.WARNING(f"Page '{source_page.title}' does not belong to any TranslationGroup. Skipping."))
                    continue

                source_locale = source.locale
                target_locale_qs = locales.exclude(id=source_locale.id)

                for target_locale in target_locale_qs:
                    # Check if translation exists
                    translated_page = translation_group.translations.filter(locale=target_locale).first()
                    if translated_page:
                        self.stdout.write(self.style.NOTICE(f"Page '{source_page.title}' already translated to '{target_locale.language_code}'. Skipping."))
                        continue

                    if dry_run:
                        self.stdout.write(self.style.SUCCESS(f"[Dry Run] Would translate '{source_page.title}' to '{target_locale.language_code}'."))
                        continue

                    # Fetch the content to translate
                    translatable_fields = ['title', 'body']  # Adjust based on your model

                    translated_data = {}
                    for field in translatable_fields:
                        original_text = getattr(source_page, field, '')
                        if original_text:
                            try:
                                translated_text = translator.translate(
                                    text=original_text,
                                    target_language=target_locale.language_code,
                                    source_language=source_locale.language_code
                                )
                                translated_data[field] = translated_text
                                self.stdout.write(self.style.SUCCESS(f"Translated '{field}': '{original_text}' -> '{translated_text}'"))
                            except Exception as e:
                                logger.error(f"Error translating field '{field}' for page '{source_page.title}': {e}")
                                self.stdout.write(self.style.ERROR(f"Failed to translate field '{field}': {e}"))
                                translated_data[field] = original_text  # Fallback to original
                        else:
                            translated_data[field] = ''

                    # Create the translated page
                    try:
                        # Duplicate the source page in the target locale
                        translated_page = translation_group.translations.create_translation(
                            locale=target_locale,
                            user=None,  # Optionally, set a user if needed
                            defaults=translated_data
                        )
                        self.stdout.write(self.style.SUCCESS(f"Successfully translated page '{source_page.title}' to '{target_locale.language_code}'"))
                    except Exception as e:
                        logger.error(f"Error creating translated page for '{source_page.title}' to '{target_locale.language_code}': {e}")
                        self.stdout.write(self.style.ERROR(f"Failed to create translated page: {e}"))

        except Exception as e:
            logger.exception("An unexpected error occurred during the translation process.")
            raise CommandError(f"An unexpected error occurred: {e}")
