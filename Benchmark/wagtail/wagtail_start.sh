#! /bin/bash

# Restart wagtail once everything is installed

cp -r ../django/untyped testsite/env/lib64/python3.10/site-packages/django

source ./testsite/env/bin/activate
cd testsite
python manage.py runserver
