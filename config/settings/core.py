import os
import environ
from pathlib import Path


env = environ.Env(
    SECRET_KEY=(str, "vo7i8az329lqc1#4x51y9-9zk3!@v!ukush8=1l=kd4jkwvj&fa#qd"),
    DEBUG=(bool, True),
    HOST=(str, "http://127.0.0.1"),
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env("SECRET_KEY")

DEBUG = env("DEBUG")

ALLOWED_HOSTS = ["resellers.beget.tech", "127.0.0.1"]

HOST = env("HOST")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third party apps

    # project apps
    "accounts",
    "company",
    "main",
    "traffic",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": env("DB__ENGINE", default="django.db.backends.sqlite3"),
        "NAME": env("DB__NAME", default=os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": env("DB__USER", default=None),
        "PASSWORD": env("DB__PASSWORD", default=None),
        "HOST": env("DB__HOST", default=None),
        "PORT": env("DB__PORT", default=None),
    }
}

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

LANGUAGE_CODE = 'uz'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True

# STATIC_URL = '/static/'
#
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = []
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]


MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "company:list"

if DEBUG:
    try:
        from .dev import *
    except ImportError:
        raise ImportError("dev settings is missing")
