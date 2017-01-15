# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try:
    from .celery import *
except ImportError as e:
    raise e

DEBUG = False
