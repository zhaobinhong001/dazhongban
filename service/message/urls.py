# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework_extensions.routers import ExtendedDefaultRouter

from service.consumer.views import ContactViewSet
from .views import GroupViewSet

router = ExtendedDefaultRouter()
(
    router.register(r'groups', GroupViewSet, base_name='im-groups').register(r'users', ContactViewSet,
        base_name='im-groups-users', parents_query_lookups=['groups_users'])
)

urlpatterns = (
    url(r'', include(router.urls)),
)
