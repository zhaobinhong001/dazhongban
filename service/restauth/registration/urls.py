# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from .views import RegisterView, VerifyMobileView

urlpatterns = (
    url(r'^$', RegisterView.as_view(), name='rest_register'),
    url(r'^verify_mobile/$', VerifyMobileView.as_view(), name='rest_verify_mobile'),
)
