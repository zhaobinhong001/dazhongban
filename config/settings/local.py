# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try:
    from .base import *
except ImportError as e:
    raise e

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '..', 'db.sqlite3'),
    },
}

if DEBUG:
    INSTALLED_APPS += (
        'debug_toolbar',
    )

    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    DEBUG_TOOLBAR_CONFIG = {'JQUERY_URL': '//cdn.bootcss.com/jquery/2.1.4/jquery.min.js'}

    # LOGGING = {
    #     'version': 1,
    #     'disable_existing_loggers': False,
    #     'handlers': {
    #         'console': {
    #             'level': 'DEBUG',
    #             'class': 'logging.StreamHandler',
    #         },
    #     },
    #     'loggers': {
    #         'django.db.backends': {
    #             'handlers': ['console'],
    #             'propagate': True,
    #             'level': 'DEBUG',
    #         },
    #     }
    # }

    # try:
    #     from .sentry import *
    # except ImportError as e:
    #     pass

