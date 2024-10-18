#! /bin/bash

# Restart wagtail once everything is installed

# first copy the ../django/shallow directory to testsite/env/lib64/python3.10/site-packages/django
cp -r ../django/shallow testsite/env/lib64/python3.10/site-packages/django

source ./testsite/env/bin/activate
cd testsite
python manage.py runserver
