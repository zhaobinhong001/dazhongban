#!/bin/sh

/usr/local/bin/python /app/manage.py migrate
/usr/local/bin/gunicorn bankpay.wsgi --worker-class=tornado -w 4 -b 0.0.0.0:4000 --chdir=/app
