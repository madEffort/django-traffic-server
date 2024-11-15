from .base import *  # noqa
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

from decouple import config  # noqa

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
        "CONN_MAX_AGE": 60,  # 최대 수명 시간 (초 단위)
    }
}


STATICFILES_DIRS = [BASE_DIR / "static"]  # 개발 환경 collectstatic 설정
