#! /bin/bash

# Restart wagtail once everything is installed

source ./testsite/env/bin/activate
cd testsite
python manage.py runserver
