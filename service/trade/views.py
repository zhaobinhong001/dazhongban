# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import QuerySet
from rest_framework import viewsets

from .models import Consumption, Contract
from .serializers import ConsumptionSerializer, ContractSerializer


class ContractViewSet(viewsets.ModelViewSet):
    '''
    合约接口
    ----
    '''
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    allowed_methods = ('POST', 'OPTION', 'HEAD')

    def get_queryset(self):
        queryset = self.queryset.filter(owner=self.request.user)

        if isinstance(queryset, QuerySet):
            queryset = queryset.all()

        return queryset


class ConsumptionViewSet(viewsets.ModelViewSet):
    '''
    消费记录接口
    ----
    '''
    queryset = Consumption.objects.all()
    serializer_class = ConsumptionSerializer
    allowed_methods = ('POST', 'OPTION', 'HEAD')

    def get_queryset(self):
        queryset = self.queryset.filter(owner=self.request.user)

        if isinstance(queryset, QuerySet):
            queryset = queryset.all()

        return queryset
