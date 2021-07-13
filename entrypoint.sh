#!/bin/sh
python django_app/manage.py makemigrations
python django_app/manage.py migrate
python django_app/manage.py createsuperuser --no-input
tail -f /dev/null