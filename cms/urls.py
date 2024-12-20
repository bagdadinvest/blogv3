from coderedcms import admin_urls as crx_admin_urls
from coderedcms import search_urls as crx_search_urls
from coderedcms import urls as crx_urls
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from wagtail.documents import urls as wagtaildocs_urls
from django.conf.urls.i18n import i18n_patterns
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# OpenAPI schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Django API",
        default_version="v1",
        description="Interactive API Documentation for Django Shell API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@dentidelil-international.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


# Define the initial urlpatterns
urlpatterns = [
    # Admin
    path("django-admin/", admin.site.urls),
    path("admin/", include(crx_admin_urls)),
    # Documents
    path("docs/", include(wagtaildocs_urls)),
    # Search view placeholder if needed
    path("search/", include(crx_search_urls)),
    path('rosetta/', include('rosetta.urls')),  # Add Rosetta
    path('api/', include('api.urls')),  # Include API routes

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

urlpatterns += [
    path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("redoc/", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
