# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import GroupViewSet, TokenViewSet

router = DefaultRouter()
router.register(r'group', GroupViewSet, base_name='im-groups')
router.register(r'token', TokenViewSet, base_name='im-token')

urlpatterns = (
    url(r'', include(router.urls)),
)
