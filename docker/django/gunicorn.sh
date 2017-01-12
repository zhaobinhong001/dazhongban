#!/bin/sh
python /app/manage.py migrate
python /app/manage.py runscript create_admin
python /app/manage.py collectstatic --noinput

/usr/bin/gunicorn config.wsgi --worker-class=tornado -w 4 -b 0.0.0.0:5000 --chdir=/app