# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework_extensions.routers import ExtendedDefaultRouter

from .views import GroupViewSet, TokenViewSet

router = ExtendedDefaultRouter()
(
    router.register(r'groups', GroupViewSet, base_name='im-groups'),
    router.register(r'token', TokenViewSet, base_name='im-token'),
)

urlpatterns = (
    url(r'', include(router.urls)),
)
