from __future__ import absolute_import, unicode_literals
import os
from pathlib import Path


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent
CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Determine if we are in production or development
IS_PRODUCTION = os.getenv('IS_PRODUCTION', 'False').lower() in ('true', '1', 't')

# Security settings
SECRET_KEY = os.getenv('SECRET_KEY', 'your-default-secret-key')
DEBUG = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# CKEditor settings
CKEDITOR_BASEPATH = "/media/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
    },
}

if IS_PRODUCTION:
    ALLOWED_HOSTS = ['172.213.217.121','dentidelil-international.com','www.dentidelil-international.com','blogtest.dentidelil-international.com']
else:
    ALLOWED_HOSTS = ['dentidelil-international.com','localhost', '127.0.0.1','172.213.217.121:443','beyondclinic.online','www.dentidelil-international.com','blogtest.dentidelil-international.com']
    
    
CSRF_TRUSTED_ORIGINS = [
    ' https://dentidelil-international.com',
] if IS_PRODUCTION else [' https://dentidelil-international.com','http://localhost:8001','http://blogtest.dentidelil-international.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql' if IS_PRODUCTION else 'django.db.backends.sqlite3',
        'NAME': os.getenv('DBNAME', BASE_DIR / 'db.sqlite3'),
        'USER': os.getenv('DBUSER', ''),
        'PASSWORD': os.getenv('DBPASS', ''),
        'HOST': os.getenv('DBHOST', ''),
        'PORT': os.getenv('DBPORT', '5432'),
    }
}

# Application definition
INSTALLED_APPS = [
    'jazzmin',  # Add this line
    'django.contrib.admin',
    'django.contrib.admindocs',  
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'corsheaders',
    'django.contrib.staticfiles',
    'apps',
    'bootstrap3',
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail',  # This replaces wagtail.core
    'modelcluster',
    'taggit',
    'ckeditor',
    'ckeditor_uploader',
    'rosetta',
    'websites',
    'actstream',
    'import_export',
    'topblogs',  # Add this line
    'django_extensions',
]

JAZZMIN_SETTINGS = {
    "site_title": "My Project Admin",
    "site_header": "My Project",
    "welcome_sign": "Welcome to the admin panel",
    "topmenu_links": [
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},
    ],
    "user_avatar": None,
    "show_ui_builder": True,
}

JAZZMIN_UI_TWEAKS = {
    "theme": "slate",
    "dark_mode_theme": "slate",
}


WAGTAIL_SITE_NAME = "beyondboard"


if DEBUG:
    
    INSTALLED_APPS.append('livereload')
    INSTALLED_APPS.append('debug_toolbar')  # Add debug_toolbar when DEBUG is True

SITE_ID = 1

MIDDLEWARE = [
    'core.middleware.DisableCSRFCheckInDevelopment',  # Add this line
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
    'livereload.middleware.LiveReloadScript',
    'core.middleware.CustomDebugToolbarMiddleware',  # Add this line
    'core.middleware.SuperuserDebugMiddleware',  # Add this line


]



INTERNAL_IPS = [
    '127.0.0.1',
]

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
LANGUAGE_COOKIE_NAME = 'django_language'

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'core.urls'
LOGIN_URL = '/apps/login/'
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Directories where Django will search for additional static files apart from app-specific ones
STATICFILES_DIRS = [
    BASE_DIR / "static",                # Global static directory
    BASE_DIR / "apps/static",           # Static directory for the 'apps' app
    BASE_DIR / "websites/static",       # Static directory for the 'websites' app
    BASE_DIR / "topblogs/static",       # Static directory for the 'topblogs' app
]

# The directory where collectstatic will collect static files for production
STATIC_ROOT = BASE_DIR / "staticfiles"

WSGI_APPLICATION = 'core.wsgi.application'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en'  # Set English as the default language

LANGUAGES = [
    ('en', 'English'),    # English as the default language
    ('fr', 'French'),
    ('ar', 'Arabic'),
    ('tr', 'Turkish'),
    ('de', 'German'),
    ('es', 'Spanish'),
    ('pl', 'Polish'),
    ('pt', 'Portuguese'),
    ('hu', 'Hungarian'),
    ('ru', 'Russian'),
]

AZURE_CLIENT_SECRET = 'f0ab28fa69a04f979d904943643d3265'

# Other relevant settings for Rosetta
ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = True

ROSETTA_MESSAGES_PER_PAGE = 500


TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = 'apps.User'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define paths relative to the project root (BASE_DIR)
WEBSITES_TEMPLATES_DIR = os.path.join(BASE_DIR, 'websites', 'site_templates')
APPS_TEMPLATES_DIR = os.path.join(BASE_DIR, 'apps', 'app_templates')
TOPBLOGS_TEMPLATES_DIR = os.path.join(BASE_DIR, 'topblogs', 'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),  # Main templates directory at project root
            os.path.join(BASE_DIR, 'templates', 'allauth'),  # allauth templates
            WEBSITES_TEMPLATES_DIR,  # Website-specific templates
            APPS_TEMPLATES_DIR,  # Apps templates directory
            TOPBLOGS_TEMPLATES_DIR,  # Top blogs templates directory
        ],
        'APP_DIRS': True,  # Allow Django to load templates from 'templates' folders in installed apps
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Localization
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'apps/locale'),
    os.path.join(BASE_DIR, 'apps/websites'),
    os.path.join(BASE_DIR, 'apps/topblogs'),

]

# Airtable and OpenAI API keys (Ensure these are secure and not exposed)
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # or 'optional', depending on your needs
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.hostinger.com'
EMAIL_PORT = 465
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'info@dentidelil-international.com'  # Your Outlook email address
EMAIL_HOST_PASSWORD = 'C19-denti123'
DEFAULT_FROM_EMAIL = 'info@dentidelil-international.com'




''''
JAZZMIN_SETTINGS = {
    # General Site Settings
    "site_title": "B-Board - Dentidelil",
    "site_header": "B-Board",
    # "site_brand": "My Brand",         # Text displayed at the top of the sidebar
    # "site_logo": "img/logo.png",      # Logo for the sidebar
    "welcome_sign": "Welcome to B-Board Dashboard",
    # "copyright": "My Company",        # Copyright info at the bottom of the sidebar

    # UI & Layout
    # "topmenu_links": [               # Custom links for the top bar (e.g., shortcuts or external links)
    #     {"name": "Home", "url": "admin:index"},
    #     {"name": "Documentation", "url": "https://docs.example.com", "new_window": True},
    # ],
     "user_avatar": "profile_image",   # Field in your User model used as the avatar image
    "show_sidebar": True,             # Show or hide the sidebar
    # "navigation_expanded": False,     # Expand or collapse the sidebar by default
    # "changeform_format": "horizontal_tabs",  # Layout for forms; options include "horizontal_tabs", "collapsible", etc.

    # Theme and Color Customization
     "theme": "darkly",               # Default theme
    # "dark_mode_theme": "darkly",      # Dark mode theme (options: "darkly", "solar", etc.)
    # "custom_css": "css/custom.css",   # Path to custom CSS file
    # "custom_js": "js/custom.js",      # Path to custom JavaScript file

    # App and Model Organization
    # "app_icon": {                     # Custom icons for each app
    #     "auth": "fas fa-users-cog",
    #     "my_app": "fas fa-project-diagram",
    # },
    # "icons": {                        # Custom icons for models
    #     "auth.user": "fas fa-user",
    #     "my_app.model_name": "fas fa-cog",
    # },

    # Sidebar Customization
    # "hide_apps": ["some_app"],        # List of apps to hide from the sidebar
    # "hide_models": ["auth.group"],    # List of models to hide from the sidebar
    # "order_with_respect_to": ["auth", "my_app"],  # Custom ordering for apps/models

    # UI Tweaks
    # "related_modal_active": True,     # Open related objects in a modal
    # "language_chooser": True,         # Add a language selector in the top bar (for multilingual sites)

    # Custom Links and Menus
    # "usermenu_links": [               # Custom links for the user profile dropdown
    #     {"name": "Support", "url": "https://support.example.com", "new_window": True},
    # ],
    # "topmenu_links": [                # Links for the top bar menu
    #     {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
    # ],

    # Footer Customization
    # "show_ui_builder": False,         # Hide or show the UI builder from Jazzmin
}
'''
