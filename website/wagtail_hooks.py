from wagtail.admin.menu import MenuItem
from wagtail import hooks
from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _
from .views import article_from_url_view  # Import your view here

@hooks.register("register_admin_urls")
def register_article_from_url():
    """
    Register the custom admin URL for scraping articles.
    """
    return [
        path("article_from_url/", article_from_url_view, name="article_from_url"),
    ]

@hooks.register("register_admin_menu_item")
def register_article_from_url_menu_item():
    """
    Add a custom menu item in the Wagtail admin panel.
    """
    return MenuItem(
        _("Article from URL"),
        reverse("article_from_url"),
        icon_name="doc-full-inverse",  # Use any Wagtail icon name
        order=102,
    )
