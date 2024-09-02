#!/bin/bash

#python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser --username=test1 --password=123321 --noinput --email='blank@email.com'

gunicorn netology_pd_diplom.wsgi:application --bind 0.0.0.0:8000