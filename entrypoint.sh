#! /bin/sh

export DJANGO_SETTINGS_MODULE=config.settings.development
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
# python manage.py runserver 0.0.0.0:8000
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3