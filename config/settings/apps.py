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
    'service.customer',
    'filters',
    'imagekit',
    'reversion',
    'easy_select2',
    'import_export',
    'daterange_filter',
)

RONGCLOUD_APPKEY = 'ik1qhw09ifflp'
RONGCLOUD_SECRET = 'kfx3v7mffJeaJt'

JPUSH_APPKEY = u'496daf24808978b12e4e0505'
JPUSH_SECRET = u'6e449bd8dd4dd2e5dff00c02'