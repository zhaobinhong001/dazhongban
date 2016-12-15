# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Contract, Transfer
from .serializers import ContractSerializer, TransferSerializer


class ContractViewSet(viewsets.ModelViewSet):
    '''
    合约接口
    ----
    '''
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = (IsAuthenticated,)
    allowed_methods = ('POST', 'OPTION', 'HEAD')

    def get_queryset(self):
        queryset = self.queryset.filter(sender=self.request.user)

        if isinstance(queryset, QuerySet):
            queryset = queryset.all()

        return queryset


class TransferViewSet(viewsets.ModelViewSet):
    '''
    消费记录接口
    ----
    '''
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = (IsAuthenticated,)
    allowed_methods = ('POST', 'OPTION', 'HEAD')

    def get_queryset(self):
        queryset = self.queryset.filter(sender=self.request.user)

        if isinstance(queryset, QuerySet):
            queryset = queryset.all()

        return queryset
