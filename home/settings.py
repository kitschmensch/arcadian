from pathlib import Path


import environ
import os


env = environ.Env()
environ.Env.read_env()
SECRET_KEY = env("SECRET_KEY")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-bx#i)u+3t#qsu)xnt$yzh(^^fnbvk=28srhx%a##cwg*e-vsm#"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = "DJANGO_DEBUG" in os.environ and os.environ

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "django_filters",
    "environ",
    "easy_tenants",
    "rest_framework",
    "rest_framework.authtoken",
    "entities",
    "home",
]

FAKER_LOCALE = None  # settings.LANGUAGE_CODE is loaded
FAKER_PROVIDERS = None  # faker.DEFAULT_PROVIDERS is loaded (all)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "home.tenant_middleware.TenantMiddleware",
]


ROOT_URLCONF = "home.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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
APPEND_SLASH = False
WSGI_APPLICATION = "home.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
"""
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "arcadian",
        "USER": "arcadianlink",
        "PASSWORD": "Wd!zTmV6MW$T!r5Vwa$kndZc5eoo3Z",
        "HOST": "localhost",
        "PORT": "",
    }
}
"""
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/


VITE_APP_DIR = BASE_DIR / "frontend"


STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "/static/"
STATICFILES_DIRS = (BASE_DIR / "home/static",)


INTERNAL_IPS = ["127.0.0.1"]


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
EASY_TENANTS_TENANT_FIELD = "tenant"
