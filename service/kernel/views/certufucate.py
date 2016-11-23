# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets
from ..models.certufucate import Certufucate
from ..serializers.certufucate import CertufucateSerializer


class CertufucateViewSet(viewsets.ModelViewSet):
    '''
    数字证书接口
    '''
    queryset = Certufucate.objects.all()
    serializer_class = CertufucateSerializer
