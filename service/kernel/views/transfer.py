# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets
from ..models.transfer import Transfer
from ..serializers.transfer import TransferSerializers


class TransferViewSet(viewsets.ModelViewSet):
    '''
    转账记录接口
    '''
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializers
    allowed_methods = ('POST', 'OPTION', 'HEAD')
