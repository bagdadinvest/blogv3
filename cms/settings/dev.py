from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "@s$j92j-_t0500=*2)&(s^b38xszk!g)z#cjz&_98#!1d#ta=n"

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = ['https://hpdev.beyond-board.me','http://127.0.0.1', 'http://192.168.1.107:3000','https://hpdev.beyond-board.me/en/','https://blog.dentidelil-international.com']

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

WAGTAIL_CACHE = False

try:
    from .local import *  # noqa
except ImportError:
    pass
