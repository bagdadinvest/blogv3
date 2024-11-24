from wagtail_localize.translation import TranslationOptions
from wagtail_localize.registry import register_translation_options
from .models import Hoca  # Import your model

@register_translation_options
class HocaTranslationOptions(TranslationOptions):
    fields = [
        'specialty',
        'description',
    ]
