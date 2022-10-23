# flake8: noqa
import os

import environ


env = environ.Env()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env.str("SECRET_KEY")
DEBUG = env.bool("DEBUG", False)
ALLOWED_HOSTS = env.str("ALLOWED_HOSTS", default="").split(" ")
CURRENTLY_HOST = env.str("CURRENTLY_HOST")
CURRENTLY_PORT = env.str("CURRENTLY_PORT")

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "phonenumber_field",
    "solo",
    "tinymce",
    "url_or_relative_url_field",
    "adminsortable2",
    "core",
    "demencia",
    "demencia_test",
    "graphene_django",
    "demencia_relatives_test",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": env.str("DB_ENGINE", "django.db.backends.sqlite3"),
        "NAME": env.str("DB_NAME", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": env.str("POSTGRES_USER", "postgres"),
        "PASSWORD": env.str("POSTGRES_PASSWORD", "postgres"),
        "HOST": env.str("DB_HOST", "localhost"),
        "PORT": env.int("DB_PORT", 5432),
    }
}


# Password validation
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
LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MAX_SIZE = env.int("MAX_SIZE")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
GRAPHENE = {"SCHEMA": "config.schema.schema"}

PHONENUMBER_DB_FORMAT = "INTERNATIONAL"
PHONENUMBER_DEFAULT_REGION = "RU"
PHONENUMBER_DEFAULT_FORMAT = "INTERNATIONAL"

EMAIL_BACKEND = env.str("EMAIL_BACKEND")
EMAIL_HOST = env.str("EMAIL_HOST")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")
DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL")
EMAIL_NAME = env.str("EMAIL_NAME")
EMAIL_PORT = env.int("EMAIL_PORT")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS")
EMAIL_FILE_PATH = os.path.join(BASE_DIR)
