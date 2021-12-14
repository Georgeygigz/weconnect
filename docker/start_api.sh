#!/bin/bash

source /root/.local/share/virtualenvs/app-*/bin/activate
export $(grep -v '^#' .env | xargs)

echo "<<<<<<<< Database Setup and Migrations Starts >>>>>>>>>"
echo ' '
echo ' '
sleep 15
python manage.py migrate


echo ' '
echo ' '
echo "<<<<<<< Collecting static files >>>>>>>>>>"
echo ' '
yes | python manage.py collectstatic --noinput

echo ' '
echo ' '
echo "<<<<<<<<<<<<<<<<<<<< START Celery >>>>>>>>>>>>>>>>>>>>>>>>"
echo ' '

# start Celery worker
celery -A app worker -l info &

echo ' '
echo ' '
echo "<<<<<<<<<<<<<<<<<<<< START API >>>>>>>>>>>>>>>>>>>>>>>>"
echo ' '
echo ' '

# Start the API with gunicorn
gunicorn --bind 0.0.0.0:8000 app.wsgi --reload --access-logfile '-' --workers 2