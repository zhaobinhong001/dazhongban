# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try:
    from .base import *
except ImportError as e:
    raise e

INSTALLED_APPS += ('raven.contrib.django.raven_compat',)

if DEBUG:
    RAVEN_CONFIG = {
        'dsn': env('RAVEN_DSN', None),
    }
