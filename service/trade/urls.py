# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import TransferViewSet, PurchasedViewSet
from service.kernel.views.consumption import ContractViewSet

router = DefaultRouter()
router.register(r'purchase', PurchasedViewSet, base_name='purchase')
# router.register(r'transfer', TransferViewSet, base_name='transfer')
router.register(r'contract', ContractViewSet, base_name='contract')

urlpatterns = (
    url(r'', include(router.urls)),
)
