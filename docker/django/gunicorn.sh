#!/bin/sh
python /app/manage.py collectstatic --noinput
python /app/manage.py migrate
/usr/bin/gunicorn config.wsgi --worker-class=tornado -w 4 -b 0.0.0.0:5000 --chdir=/app