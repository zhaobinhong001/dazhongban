# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from psycopg2.extensions import ISOLATION_LEVEL_SERIALIZABLE

try:
    from .base import *
except ImportError, e:
    raise e


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('POSTGRES_USER', default='bankeys'),
        'USER': env('POSTGRES_USER', default='bankeys'),
        'PASSWORD': env('POSTGRES_PASSWORD', default='secret'),
        'HOST': env('POSTGRES_HOST', default='localhost'),
        'PORT': env('POSTGRES_PORT', default='5432'),
        'OPTIONS': {
            'isolation_level': ISOLATION_LEVEL_SERIALIZABLE,
            'client_encoding': 'UTF8',
        },
        'timezone': 'UTC',
    }
}

DATABASES['default'] = env.db('DATABASE_URL', default=DATABASES['default'])

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': env('CELERY_BROKER_URL', default='127.0.0.1:6379'),
        'OPTIONS': {
            'DB': 0,
            'PASSWORD': '',
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 50,
                'timeout': 20,
            }
        },
    },
}


DEBUG = True






