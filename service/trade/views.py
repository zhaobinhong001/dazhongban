# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from service.trade.models import Purchased
from service.trade.serializers import PurchasedSerializer, ContractDetailSerializer

from .models import Contract, Transfer
from .serializers import ContractSerializer, TransferSerializer


class ContractViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    合约接口
    ----

    合约类型

    ('transfer', '转账'),
    ('receiver', '收款'),
    ('thirty', '第三方支付'),
    ('receipt', '收据'),
    ('borrow', '借条'),
    ('owe', '欠条'),



    '''
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = (IsAuthenticated,)
    # allowed_methods = ('POST', 'OPTION', 'HEAD')

    # def perform_create(self, serializer):
    #     serializer.save(sender=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = ContractDetailSerializer
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = self.queryset.filter(sender=self.request.user)

        if isinstance(queryset, QuerySet):
            queryset = queryset.all()

        return queryset


class TransferViewSet(viewsets.ModelViewSet):
    '''
    转账支付接口
    ----

    转账状态 status = ('', '无状态'), ('agree', '同意'), ('reject', '拒绝')
    转账类型 type = ('transfer', '转账'),('receiver', '收款'),('thirty', '第三方'),
    '''
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = (IsAuthenticated,)
    allowed_methods = ('POST', 'OPTION', 'HEAD')

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def get_queryset(self):
        queryset = self.queryset.filter(sender=self.request.user)

        if isinstance(queryset, QuerySet):
            queryset = queryset.all()

        return queryset


class PurchasedViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = PurchasedSerializer
    queryset = Purchased.objects.all()