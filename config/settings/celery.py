# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try:
    from .base import *
except ImportError as e:
    raise e

DEBUG = False
INSTALLED_APPS += ("django_celery_results", 'django_celery_beat',)

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TASK_SERIALIZER = 'json'
