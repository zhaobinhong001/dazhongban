# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import q, qs, scan_login

urlpatterns = [
    url(r'^q/(?P<uid>.*)/$', q, name='q'),
    url(r'^qs/(?P<key>.*)/$', qs, name='qs'),
    url(r'^scan_login/', scan_login, name='scan_login'),
]
