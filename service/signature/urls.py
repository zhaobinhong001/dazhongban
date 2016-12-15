# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import VerifyViewSet, HistoryViewSet, IdentityViewSet, ValidateViewSet, BankcardViewSet, CallbackViewSet

router = DefaultRouter()
router.register(r'history', HistoryViewSet, base_name='history')
router.register(r'signature', VerifyViewSet, base_name='signature')
router.register(r'bankcard', BankcardViewSet, base_name='bankcard')
router.register(r'callback', CallbackViewSet, base_name='callback')
router.register(r'validate', ValidateViewSet, base_name='validate')
router.register(r'identity', IdentityViewSet, base_name='identity')

urlpatterns = (
    url(r'', include(router.urls)),
)
