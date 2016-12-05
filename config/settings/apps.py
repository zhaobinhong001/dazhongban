# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .base import INSTALLED_APPS

INSTALLED_APPS += (
    'service.frontend',
    'service.trade',
    'service.kernel',
    'service.message',
    'service.consumer',
    'service.restauth',
    'service.signature',
    'service.restauth.registration',
    'service.dashboard',

    'imagekit',
    'reversion',
    'easy_select2',
    'import_export',
    'daterange_filter',
)

RONGCLOUD_APPKEY = 'ik1qhw09ifflp'
RONGCLOUD_SECRET = 'kfx3v7mffJeaJt'
