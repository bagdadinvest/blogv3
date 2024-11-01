from .base import *  # noqa
from dotenv import load_dotenv
load_dotenv()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = ['https://hpdev.beyond-board.me','http://127.0.0.1', 'http://192.168.1.107:3000','https://hpdev.beyond-board.me/en/','https://blog.dentidelil-international.com','https://dentidelil-international.com']

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Secret key
SECRET_KEY = os.getenv("SECRET_KEY")

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

WAGTAIL_CACHE = False

try:
    from .local import *  # noqa
except ImportError:
    pass
