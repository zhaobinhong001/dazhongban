# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.db.models import QuerySet
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from url_filter.integrations.drf import DjangoFilterBackend

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


    时间过滤规则：
    在 url 后面加 ?created__range=<start_date>,<end_date>
    例如: ?created__range=2010-01-01,2016-12-31
    '''

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filter_fields = ['created']

    ordering_fields = ('created',)
    ordering = ('id',)
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        self.queryset = self.queryset
        self.serializer_class = ContractDetailSerializer
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(Q(sender=self.request.user) | ~Q(status='normal'))
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = self.queryset

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
