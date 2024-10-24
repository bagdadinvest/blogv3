from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "@s$j92j-_t0500=*2)&(s^b38xszk!g)z#cjz&_98#!1d#ta=n"

# Add your site's domain name(s) here.
ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1', 'http://192.168.1.107:3000']

# To send email from the server, we recommend django_sendmail_backend
# Or specify your own email backend such as an SMTP server.
# https://docs.djangoproject.com/en/5.0/ref/settings/#email-backend
# EMAIL_BACKEND = "django_sendmail_backend.backends.EmailBackend"

# Default email address used to send messages from the website.
DEFAULT_FROM_EMAIL = "dentiblog <info@dentidelil-international.com>"

# A list of people who get error notifications.
ADMINS = [
    ("Administrator", "admin@dentidelil-international.com"),
]

# A list in the same format as ADMINS that specifies who should get broken link
# (404) notifications when BrokenLinkEmailsMiddleware is enabled.
MANAGERS = ADMINS

# Email address used to send error messages to ADMINS.
SERVER_EMAIL = DEFAULT_FROM_EMAIL

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": BASE_DIR / "cache",  # noqa
        "KEY_PREFIX": "coderedcms",
        "TIMEOUT": 14400,  # in seconds
    }
}
