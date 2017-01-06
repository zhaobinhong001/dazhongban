# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

try:
    from .base import *
except ImportError as e:
    raise e

MEDIA_URL = '/media/'
STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'assets', 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'assets', 'media')
THUMB_ROOT = os.path.join(BASE_DIR, '..', 'assets', 'media', 'thumb')

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
