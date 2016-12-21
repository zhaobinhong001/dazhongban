# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import q, check, qs, expiration, success, scan_login

urlpatterns = [
    url(r'^q/(?P<uid>.*)/$', q, name='q'),
    url(r'^qs/(?P<key>.*)/$', qs, name='qs'),
    url(r'^check/(?P<key>.*)/$', check, name='check'),
    url(r'^scan_login/', scan_login, name='scan_login'),
    url(r'^success/', success, name='success'),
    url(r'^expiration/', expiration, name='expiration'),
]
