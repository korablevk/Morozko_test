from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "debug_toolbar",
    'mathfilters',
    'crispy_forms',
    "crispy_bootstrap5",
    'django_email_verification',

    "main",
    "products",
    "cart",
    "accounts",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "settings.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",


                'cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = "settings.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
DEFAULT_PORT = 5432
DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_NAME'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': int(os.environ.get('POSTGRES_PORT',DEFAULT_PORT)),
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": BASE_DIR / "cache",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / 'static'
    ]

MEDIA_URL = 'media/'

MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = 'accounts.User'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


#Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"



def email_verified_callback(user):
    user.is_active = True


# def password_change_callback(user, password):
#     user.set_password(password)


# Mandatory email settings
EMAIL_FROM_ADDRESS = os.environ.get('EMAIL_FROM_ADDRESS', 'default_email@example.com')  
EMAIL_PAGE_DOMAIN = os.environ.get('EMAIL_PAGE_DOMAIN', 'http://example.com')  

# Optional settings with proper default values
EMAIL_MULTI_USER = os.environ.get('EMAIL_MULTI_USER', 'False').lower() == 'true'  

# Email Verification Settings
EMAIL_MAIL_SUBJECT = 'Confirm your email {{ user.username }}'
EMAIL_MAIL_HTML = 'accounts/email/mail_body.html'
EMAIL_MAIL_PLAIN = 'accounts/email/mail_body.txt'
EMAIL_MAIL_TOKEN_LIFE = 60 * 60  # 1 hour in seconds

EMAIL_MAIL_PAGE_TEMPLATE = 'accounts/email/email_success_template.html'
EMAIL_MAIL_CALLBACK = email_verified_callback

# Email Backend Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  
DEFAULT_EMAIL_PORT = 587

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', DEFAULT_EMAIL_PORT))  
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'default_user@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'default_password')  
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true'

# Debug email during development (logs emails to the console instead of sending them)
if os.environ.get('DEBUG', 'True').lower() == 'true':  
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
