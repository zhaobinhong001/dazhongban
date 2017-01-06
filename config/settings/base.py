# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os

import environ

ROOT_DIR = environ.Path(__file__) - 3
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# environ.Env.read_env()
env = environ.Env()

SECRET_KEY = env('DJANGO_SECRET_KEY', default='s4lk7ni)@9n0+4a!2_$vss8hqks_0#f_ia%i8k!djc87y$@0x5')

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin.apps.SimpleAdminConfig',
    'django.contrib.admindocs',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django_extensions',
    'suit_dashboard',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

SITE_ID = 1
ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DEFAULT_CHARSET = 'utf-8'
LANGUAGE_CODE = 'zh-hans'
ENCODING = 'zh-hans'

USE_I18N = True
USE_L10N = False

DATETIME_FORMAT = 'Y-m-d H:i:s'
DATE_FORMAT = 'Y-m-d'
USE_TZ = False

try:
    from .apps import *
    from .auth import *
    from .rest import *
    from .suit import *

    from .static import *
    from .celery import *

    # from .cache import *
    from .thumb import *

except ImportError as e:
    raise e
