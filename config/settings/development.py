from .base import *  # noqa
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


STATICFILES_DIRS = [BASE_DIR / "static"]  # 개발 환경 collectstatic 설정
