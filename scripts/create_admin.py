# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import environ
from django.contrib.auth import get_user_model

ROOT_DIR = environ.Path(__file__) - 2

env = environ.Env()
env.read_env(str(ROOT_DIR.path('.env')))


def run():
    try:
        admin = get_user_model()(username=env('DJANGO_ADMIN_USER', default='admin'))
        admin.set_password(env('DJANGO_ADMIN_PASS', default='admin'))
        admin.is_superuser = True
        admin.is_staff = True
        admin.save()
    except Exception as e:
        print u'用户已经存在'
