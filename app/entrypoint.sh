#!/bin/bash

# Collect static files
echo "Collect static files"
npm -v && python manage.py tailwind install --no-input
python manage.py tailwind build --no-input
python manage.py collectstatic --no-input

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Starting server"
gunicorn challenge_weekbier.wsgi:application --bind 0.0.0.0:5000

