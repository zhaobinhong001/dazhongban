# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time

import datetime

from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from service.frontend.models import QRToken

from django.conf import settings

from service.kernel.serializers.shared import ScanSerializer


class QRLoginViewSet(viewsets.GenericViewSet):
    '''
    扫码验证接口


    '''
    queryset = QRToken.objects.all()
    serializer_class = ScanSerializer
    permission_classes = (IsAuthenticated,)

    @detail_route(methods=['GET'])
    def done(self, request, pk, *args, **kwargs):
        '''
        扫码成功

        '''
        # 获取用户
        owner = request.user

        # 更新状态为done
        QRToken.objects.filter(key=pk).update(owner=owner, status='done')

        return Response({'status': 'done'})

    @detail_route(methods=['GET'])
    def check(self, request, pk, *args, **kwargs):
        '''
        查询状态,js 调用

        '''
        # 获取二维码信息
        obj = QRToken.objects.filter(key=pk).get()

        # 计算二维码生成时间
        nowTime = int(time.mktime(datetime.datetime.now().timetuple()))
        created = int(time.mktime(obj.created.timetuple()))
        expired = nowTime - created

        # 判断是否超时
        if expired >= settings.SCAN_TIMEOUT:
            QRToken.objects.filter(key=pk).delete()
            return Response({'status': 'timeout'})

        return Response({'status': obj.status})

    @detail_route(methods=['GET'])
    def cancel(self, request, pk, *args, **kwargs):
        '''
        取消登陆

        '''
        # 更新状态为cancel
        QRToken.objects.filter(key=pk).update(status='cancel')

        return Response({'status': 'cancel'})

    @detail_route(methods=['GET'])
    def scan(self, request, pk, *args, **kwargs):
        '''
        已经扫码

        '''
        # 更新状态为scan
        QRToken.objects.filter(key=pk).update(status='scan')

        return Response({'status': 'scan'})
