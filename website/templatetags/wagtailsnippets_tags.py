from django import template
from ..models import PortfolioSnippet, AboutUsSnippet, ServiceSnippet, PatientJourneySnippet, PricingSnippet, Hoca,Sponsor, LocalizedFooter, FooterWithForm, FAQ

register = template.Library()

@register.simple_tag
def get_portfolio_items():
    """Returns all portfolio items"""
    return PortfolioSnippet.objects.all()

@register.simple_tag
def get_about_us():
    """Returns About Us snippets"""
    return AboutUsSnippet.objects.all()

@register.simple_tag
def get_services():
    """Returns all service snippets"""
    return ServiceSnippet.objects.all()

@register.simple_tag
def get_patient_journeys():
    """Returns all patient journey snippets"""
    return PatientJourneySnippet.objects.all()

@register.simple_tag
def get_pricing_items():
    """Returns all pricing snippets"""
    return PricingSnippet.objects.all()

@register.simple_tag
def get_hocas():
    """Returns all doctor snippets ordered by number"""
    return Hoca.objects.all().order_by('number')

@register.simple_tag
def get_sponsors():
    """Returns all sponsor snippets"""
    return Sponsor.objects.all()

register.simple_tag
def get_footer():
    """Returns the localized footer snippet"""
    return LocalizedFooter.objects.first()


@register.simple_tag
def get_footer():
    try:
        return FooterWithForm.objects.first()  # Or filter for specific conditions
    except FooterWithForm.DoesNotExist:
        return None


@register.simple_tag
def get_faq_items(faq_id=None):
    """
    Returns FAQ items for a specific FAQ snippet or all FAQ snippets.
    """
    if faq_id:
        try:
            faq = FAQ.objects.get(id=faq_id)
            faq_items = faq.faq_items.all()
            print(f"Found {faq_items.count()} items for FAQ ID {faq_id}")
            return faq_items
        except FAQ.DoesNotExist:
            print(f"FAQ with ID {faq_id} does not exist.")
            return []
    else:
        # If no specific FAQ ID is provided, fetch items from all FAQ snippets.
        faq_items = FAQ.objects.prefetch_related("faq_items").all()
        print(f"Found {faq_items.count()} FAQ items in total.")
        return faq_items
