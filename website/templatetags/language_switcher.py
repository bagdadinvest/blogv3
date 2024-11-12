from django import template
from wagtail.models import Locale
from wagtail.models import Page

register = template.Library()

@register.simple_tag(takes_context=True)
def language_switcher(context, lang_code):
    request = context['request']
    current_page = context.get('page')  # Get the current page from context

    # Check if the page exists in the current context and if translated versions are available
    if current_page and hasattr(current_page, 'get_translation'):
        try:
            # Try to get the translation of the current page for the desired locale
            target_locale = Locale.objects.get(language_code=lang_code)
            translated_page = current_page.get_translation(target_locale)

            # If the translated page exists, return its URL
            return translated_page.get_url(request)
        except Locale.DoesNotExist:
            # If the target locale does not exist, return the current URL (fallback)
            return request.path
        except Page.DoesNotExist:
            # If the translated page does not exist, return the current URL (fallback)
            return request.path

    # If no page is found in the context or it's not translatable, return the current path
    return request.path
