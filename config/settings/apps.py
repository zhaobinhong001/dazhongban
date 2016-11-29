# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .base import INSTALLED_APPS, DEBUG

INSTALLED_APPS += (
    'service.frontend',
    'service.kernel',
    'service.message',
    'service.consumer',
    'service.restauth',
    'service.restauth.registration',

    'imagekit',
    'reversion',
    'easy_select2',
    'import_export',
)


RONGCLOUD_APPKEY = 'ik1qhw09ifflp'
RONGCLOUD_SECRET = 'kfx3v7mffJeaJt'