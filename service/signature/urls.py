# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework_extensions.routers import ExtendedDefaultRouter

from .views import VerifyViewSet, HistoryViewSet, CertificateViewSet

# router = DefaultRouter()
router = ExtendedDefaultRouter()
(
    router.register(r'certs', CertificateViewSet, base_name='certs'),
    router.register(r'verify', VerifyViewSet, base_name='verify'),
    router.register(r'history', HistoryViewSet, base_name='history'),
)

# router.register(r'group', GroupViewSet, 'im-group')
# router.register(r'contact', ContactViewSet, 'me-contact')
# router.register(r'bankcard', BankcardViewSet, 'me-bankcard')
# router.register(r'blacklist', BlacklistViewSet, 'me-blacklist')
# router.register(r'signatures', SignatureViewSet, 'me-signatures')
# router.register(r'treaties', TreatyViewSet, 'me-treaties')
# router.register(r'trades', TradeViewSet, 'me-trades')

urlpatterns = (
    url(r'^', include(router.urls)),
    # url(r'^profile/$', ProfileViewSet.as_view(), name='me-profile'),
    # url(r'^avatar/$', AvatarViewSet.as_view(), name='me-avatar'),
    # url(r'^settings/$', SettingsViewSet.as_view(), name='me-settings'),
)
