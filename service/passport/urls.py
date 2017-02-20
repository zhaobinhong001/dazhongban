# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import SigninViewSet, SignupViewSet, PaymentViewSet, ReceiveViewSet, RefundsViewSet, PushViewSet

router = DefaultRouter()
router.register(r'signin', SigninViewSet, base_name='signin')
router.register(r'signup', SignupViewSet, base_name='signup')
router.register(r'payment', PaymentViewSet, base_name='payment')
router.register(r'receive', ReceiveViewSet, base_name='receive')
router.register(r'refunds', RefundsViewSet, base_name='refunds')
router.register(r'push', PushViewSet, base_name='push')

urlpatterns = (
    url(r'', include(router.urls)),
    # url(r'push', PushView.as_view())
)
