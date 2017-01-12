# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try:
    from .base import *
except ImportError as e:
    raise e

INSTALLED_APPS += (
    "django_celery_results",
    'django_celery_beat',
)

DEBUG = False
CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='redis://localhost:6379/0')

CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
