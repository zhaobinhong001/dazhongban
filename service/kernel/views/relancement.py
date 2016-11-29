# coding:utf-8
from __future__ import unicode_literals
from rest_framework import viewsets
from ..models.relancement import Relancement
from ..serializers.relancement import RelancementSerializer


class RelancementViewSet(viewsets.ModelViewSet):
    '''
    创建公告
    '''
    queryset = Relancement.objects.all()
    serializer_class = RelancementSerializer
    allowed_methods = ('POST', 'OPTION', 'HEAD')
