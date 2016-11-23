# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import ProfileViewSet, AvatarViewSet, AddressViewSet, ContactViewSet

router = DefaultRouter()
router.register(r'address', AddressViewSet, 'me-address')
router.register(r'contact', ContactViewSet, 'me-contact')

# router.register(r'signatures', SignatureViewSet, 'me-signatures')
# router.register(r'treaties', TreatyViewSet, 'me-treaties')
# router.register(r'trades', TradeViewSet, 'me-trades')

urlpatterns = (
    url(r'^', include(router.urls)),
    url(r'^profile/$', ProfileViewSet.as_view(), name='me-profile'),
    url(r'^avatar/$', AvatarViewSet.as_view(), name='me-avatar'),
)
