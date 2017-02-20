# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import HistoryViewSet, IdentityViewSet, ValidateViewSet, BankcardViewSet, CallbackViewSet, SignatureViewSet, \
    CertificateViewSet,CounterViewSet

router = DefaultRouter()
router.register(r'history', HistoryViewSet, base_name='history')
router.register(r'signature', SignatureViewSet, base_name='signature')
router.register(r'bankcard', BankcardViewSet, base_name='bankcard')
router.register(r'callback', CallbackViewSet, base_name='callback')
router.register(r'validate', ValidateViewSet, base_name='validate')
router.register(r'identity', IdentityViewSet, base_name='identity')
router.register(r'counter', CounterViewSet, base_name='counter')

router.register(r'certificate', CertificateViewSet, base_name='certificate')

urlpatterns = (
    url(r'', include(router.urls)),
)
