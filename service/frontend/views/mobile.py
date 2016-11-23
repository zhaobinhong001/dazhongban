# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


