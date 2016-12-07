# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import ProfileViewSet, AvatarViewSet, AddressViewSet, ContactViewSet, BankcardViewSet, BlacklistViewSet, \
    SettingsViewSet, NickViewSet

router = DefaultRouter()
router.register(r'address', AddressViewSet, 'me-address')
router.register(r'contact', ContactViewSet, 'me-contact')
router.register(r'bankcard', BankcardViewSet, 'me-bankcard')
router.register(r'blacklist', BlacklistViewSet, 'me-blacklist')

urlpatterns = (
    url(r'^', include(router.urls)),
    url(r'^nick/$', NickViewSet.as_view(), name='me-nick'),
    url(r'^avatar/$', AvatarViewSet.as_view(), name='me-avatar'),
    url(r'^profile/$', ProfileViewSet.as_view(), name='me-profile'),
    url(r'^settings/$', SettingsViewSet.as_view(), name='me-settings'),
)
