"""
Django settings for Fermento project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import base64
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY') if os.getenv('SECRET_KEY') else 'INSECURE_STANDARD_KEY_SET_IN_ENV'
FIELD_ENCRYPTION_KEY = base64.urlsafe_b64encode(SECRET_KEY.encode())
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', False) == 'True'

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'Apps.batches',
    'Apps.recipe_manager',
    'Fermento',
    'Apps.settings_manager',
    'Apps.restapi_manager',

    'lineage',
    'widget_tweaks',
    'easy_thumbnails',
    'image_cropping',

    'django_cleanup.apps.CleanupConfig',
    'qr_code',
    'encrypted_model_fields',
    'drf_yasg',
    'rest_framework',
    'django_filters',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',

]

ROOT_URLCONF = 'Fermento.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'datetime': 'Fermento.modules.datetime',
            }
        },
    },
]

WSGI_APPLICATION = 'Fermento.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "data" / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LANGUAGES = [('en', 'English'), ('de', 'Deutsch')]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'Fermento', 'locale'),
    os.path.join(BASE_DIR, 'Apps/recipe_manager', 'locale'),
    os.path.join(BASE_DIR, 'Apps/batches', 'locale'),
    os.path.join(BASE_DIR, 'templates', 'locale'),
    os.path.join(BASE_DIR, 'static', 'custom', 'js', 'locale'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = BASE_DIR / 'data' / 'media'

MEDIA_URL = '/media/'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DATETIME_FORMAT': "%Y-%m-%dT%H:%M",
}

CSRF_TRUSTED_ORIGINS = [
    # 'http://localhost:6733',
    # 'http://127.0.0.1:6733',
    os.getenv('APP_URL') if os.getenv('APP_URL') else 'http://127.0.0.1:6733',
]
CORS_ORIGIN_WHITELIST = [
    # 'http://localhost:6733',
    # 'http://127.0.0.1:6733',
    os.getenv('APP_URL') if os.getenv('APP_URL') else 'http://127.0.0.1:6733',
]
from easy_thumbnails.conf import Settings as thumbnail_settings

THUMBNAIL_PROCESSORS = (
                           'image_cropping.thumbnail_processors.crop_corners',
                       ) + thumbnail_settings.THUMBNAIL_PROCESSORS

### Configuration values ###
SHOW_EMPTY_PROCESS_CATEGORIES = False
SCHEDULE_UPDATE_INTERVAL = os.getenv("SCHEDULE_UPDATE_INTERVAL") if "SCHEDULE_UPDATE_INTERVAL" in os.environ else 1
TIME_ZONE = os.getenv("TIMEZONE") if "TIMEZONE" in os.environ else "Europe/Berlin"

# Images
DOWNSIZE_IMAGES = bool(os.getenv("DOWNSIZE_IMAGES")) if "DOWNSIZE_IMAGES" in os.environ else True
MAX_IMAGE_WIDTH = int(os.getenv("MAX_IMAGE_WIDTH")) if "MAX_IMAGE_WIDTH" in os.environ else 600
### End ###
