# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import VerifyViewSet, HistoryViewSet, IdentityViewSet, ValidateViewSet, BankcardViewSet

router = DefaultRouter()
router.register(r'verify', VerifyViewSet, base_name='verify')
router.register(r'history', HistoryViewSet, base_name='history')
router.register(r'bankcard', BankcardViewSet, base_name='bankcard')
router.register(r'callback', ValidateViewSet, base_name='callback')
router.register(r'identity', IdentityViewSet, base_name='identity')

urlpatterns = (
    url(r'', include(router.urls)),
)
