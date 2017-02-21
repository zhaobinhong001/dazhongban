#!/bin/sh

/bin/python /app/manage.py migrate
/bin/gunicorn bankpay.wsgi --worker-class=tornado -w 4 -b 0.0.0.0:5000 --chdir=/app