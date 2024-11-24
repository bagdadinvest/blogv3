from coderedcms import admin_urls as crx_admin_urls
from coderedcms import search_urls as crx_search_urls
from coderedcms import urls as crx_urls
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from wagtail.documents import urls as wagtaildocs_urls
from django.conf.urls.i18n import i18n_patterns

# Define the initial urlpatterns
urlpatterns = [
    # Admin
    path("django-admin/", admin.site.urls),
    path("admin/", include(crx_admin_urls)),
    # Documents
    path("docs/", include(wagtaildocs_urls)),
    # Search view placeholder if needed
    path("search/", include(crx_search_urls)),
]

# Add i18n patterns
urlpatterns += i18n_patterns(
    path("", include(crx_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath of your site:
    # path("pages/", include(wagtail_urls)),
)

# Additional settings for development
if settings.DEBUG:
    from django.conf.urls.static import static
    import debug_toolbar

    # Serve static and media files from the development server
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # type: ignore
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # type: ignore

    # Add debug toolbar URLs
    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
