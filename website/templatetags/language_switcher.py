from django import template
from wagtail.models import Locale

register = template.Library()


@register.inclusion_tag('language_switcher.html', takes_context=True)
def language_switcher(context):
    """
    Generates a list of available languages with their URLs and identifies the current language.
    """
    request = context['request']
    current_page = context.get('page', None)
    language_links = []
    current_language = None

    # Get all available locales
    locales = Locale.objects.all()

    for locale in locales:
        try:
            # Determine the URL for the translated page
            if current_page and hasattr(current_page, 'get_translation'):
                translated_page = current_page.get_translation(locale)
                url = translated_page.get_url(request)
            else:
                url = request.path

            # Add the language details to the list
            language_links.append({
                'language_code': locale.language_code,
                'language_name': locale.get_display_name(),
                'url': url
            })

            # Identify the current language
            if locale.language_code == context.get('LANGUAGE_CODE'):
                current_language = {
                    'language_code': locale.language_code,
                    'language_name': locale.get_display_name(),
                }
        except Exception:
            # Handle cases where translation or locale might not exist
            language_links.append({
                'language_code': locale.language_code,
                'language_name': locale.get_display_name(),
                'url': request.path
            })

    return {
        'language_links': language_links,
        'current_lang': current_language,
    }
