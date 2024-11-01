# middleware.py in your Django app
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

class DisableCSRFCheckInDevelopment(MiddlewareMixin):
    def process_request(self, request):
        if not settings.IS_PRODUCTION:
            setattr(request, '_dont_enforce_csrf_checks', True)

# custom_toolbar_middleware.py
from django.conf import settings
from debug_toolbar.middleware import DebugToolbarMiddleware

class CustomDebugToolbarMiddleware(DebugToolbarMiddleware):
    def __call__(self, request):
        # Check if the user is authenticated and is a superuser or admin
        if request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff):
            # Enable Debug Toolbar
            return super().__call__(request)
        else:
            # If the user is not authorized, simply pass through the request
            response = self.get_response(request)
            return response


# myapp/middleware.py

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

class SuperuserDebugMiddleware(MiddlewareMixin):
    """
    Middleware to temporarily enable DEBUG mode for superusers.
    """
    def process_request(self, request):
        # Set `request.debug` context for superusers
        request.debug = request.user.is_authenticated and request.user.is_superuser

        # Temporarily enable DEBUG mode for superusers
        if request.debug:
            settings.DEBUG = True
        else:
            settings.DEBUG = False
