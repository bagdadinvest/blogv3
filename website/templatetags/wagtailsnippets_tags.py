from django import template
from ..models import PortfolioSnippet, AboutUsSnippet, ServiceSnippet, PatientJourneySnippet, PricingSnippet

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
