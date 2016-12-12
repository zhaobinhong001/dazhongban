# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try:
    from .base import INSTALLED_APPS
except ImportError as e:
    raise e


INSTALLED_APPS += ("django_celery_results", 'django_celery_beat',)
# CELERY_RESULT_BACKEND = 'django-db'
# CELERY_RESULT_BACKEND = 'django-cache'

CELERY_BROKER_URL = 'redis://localhost:6379/0'

#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TASK_SERIALIZER = 'json'