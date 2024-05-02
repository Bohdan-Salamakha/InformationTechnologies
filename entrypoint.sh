#!/bin/sh
poetry run python manage.py collectstatic --noinput
poetry run python manage.py migrate
poetry run gunicorn information_technologies.wsgi:application --bind 0.0.0.0:8000
