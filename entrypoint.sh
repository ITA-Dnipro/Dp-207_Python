#!/bin/sh
python django_app/manage.py makemigrations
python django_app/manage.py migrate
python django_app/manage.py createsuperuser --no-input
cd django_app/ && celery -A django_app worker -B -l INFO
tail -f /dev/null