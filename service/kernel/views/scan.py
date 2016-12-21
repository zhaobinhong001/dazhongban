# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from service.consumer.serializers import UserSerializer
from service.frontend.models import QRToken


class ScanViewSet(viewsets.ModelViewSet):
    '''
    扫码验证接口

    '''
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    @detail_route(methods=['POST', 'GET', 'PUT'])
    def binding_code(self, request, pk, *args, **kwargs):
        owner = request.user
        QRToken.objects.filter(key=pk).update(owner=owner)

        return Response({'detail': '操作成功'}, status=status.HTTP_201_CREATED)
