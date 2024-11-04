from .base import *  # noqa
from decouple import config

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

DB_NAME = config("DB_NAME", cast=str)
DB_USER = config("DB_USER", cast=str)
DB_PASSWORD = config("DB_PASSWORD", cast=str)
DB_HOST = config("DB_HOST", cast=str)
DB_PORT = config("DB_PORT", cast=str)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": DB_NAME,
        "USER": DB_USER,
        "PASSWORD": DB_PASSWORD,
        "HOST": DB_HOST,
        "PORT": DB_PORT,
    }
}
