# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .base import INSTALLED_APPS, DEBUG

INSTALLED_APPS += ('raven.contrib.django.raven_compat',)

if DEBUG:
    RAVEN_CONFIG = {
        'dsn': 'http://e5a9ee5b466345618091bd18aafc65aa:c645518f9522416db14d37cbe0e3bfb1@101.200.136.70:9000/3',
        # 'release': fetch_git_sha(os.path.abspath(os.path.join(BASE_DIR, '..'))),
    }
