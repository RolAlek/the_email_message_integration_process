#!/bin/sh

python /app/the_message_integration_project/manage.py makemigrations --no-input
python /app/the_message_integration_project/manage.py migrate --no-input

python /app/the_message_integration_project/manage.py runserver 0.0.0.0:8000