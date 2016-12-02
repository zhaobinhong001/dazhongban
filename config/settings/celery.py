# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try:
    from .base import INSTALLED_APPS
except ImportError as e:
    raise e


INSTALLED_APPS += ("django_celery_results", 'django_celery_beat',)
CELERY_RESULT_BACKEND = 'django-db'
# CELERY_RESULT_BACKEND = 'django-cache'