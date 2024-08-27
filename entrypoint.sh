#!/bin/bash

python manage.py collectstatic
python manage.py migrate
gunicorn netology_pd_diplom.wsgi:application --bind 0.0.0.0:8000