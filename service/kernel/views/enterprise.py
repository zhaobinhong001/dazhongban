# coding:utf-8
from __future__ import unicode_literals
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from service.kernel.serializers.enterprise import enterpriseSerialzer
from service.kernel.models.enterprise import EnterpriseUser


class EnterproseViewSet(viewsets.ModelViewSet):
    '''
    企业用户接口
    '''
    queryset = EnterpriseUser.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = enterpriseSerialzer
    allowed_methods = ('POST', 'OPTION', 'HEAD')
