# coding:utf-8
from __future__ import unicode_literals
from rest_framework import viewsets
from ..models.consumption import Consumption
from ..serializers.consumption import ConsumptionSerializer


class ConsumptionViewSet(viewsets.ModelViewSet):
    '''
    消费记录接口
    '''
    queryset = Consumption.objects.all()
    serializer_class = ConsumptionSerializer
    allowed_methods = ('POST', 'OPTION', 'HEAD')
