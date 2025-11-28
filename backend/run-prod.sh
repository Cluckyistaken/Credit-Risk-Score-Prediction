#!/bin/sh
python manage.py migrate
gunicorn backend_project.wsgi:application --bind 0.0.0.0:8000
