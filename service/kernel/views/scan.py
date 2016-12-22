# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time

import datetime
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from service.frontend.models import QRToken
import json

from service.kernel.serializers.scan import ScanSerializer


class ScanViewSet(viewsets.ModelViewSet):
    '''
    扫码验证接口

    '''
    queryset = get_user_model().objects.all()
    serializer_class = ScanSerializer

    permission_classes = (IsAuthenticated,)

    @detail_route(methods=['PUT'])
    def done(self, request, pk, *args, **kwargs):
        '''
        扫码确认登陆

        '''
        owner = request.user
        QRToken.objects.filter(key=pk).update(owner=owner, status='done')
        data = {'type': '确认登陆', 'data': 'done'}
        in_json = json.dumps(data).encode("hex")
        return Response(in_json)

    @detail_route(methods=['GET'])
    def scan(self, request, pk, *args, **kwargs):
        '''
        监听扫码前的动作

        '''
        obj = QRToken.objects.filter(key=pk).get()
        nowTime = int(time.mktime(datetime.datetime.now().timetuple()))
        created = int(time.mktime(obj.created.timetuple()))
        isexpiration = nowTime - created

        try:

            if isexpiration > 60:
                data = {'type': '超时', 'data': 'timeout'}
                in_json = json.dumps(data)
                return Response(in_json)
            elif obj.status == 'done':
                data = {'type': '扫码成功等待用户操作', 'data': 'done'}
                in_json = json.dumps(data)
                return Response(in_json)
            elif obj.status == 'cancel':
                data = {'type': '取消登陆', 'data': 'cancel'}
                in_json = json.dumps(data)
                return Response(in_json)
            elif obj.status == 'scan':
                data = {'type': '等待扫码', 'data': 'scan'}
                in_json = json.dumps(data)
                return Response(in_json)

        except QRToken.DoesNotExist:
            raise Exception()

    @detail_route(methods=['PUT'])
    def cancel(self, request, pk, *args, **kwargs):
        '''
        取消登陆

        '''
        QRToken.objects.filter(key=pk).update(status='cancel')
        data = {'type': '取消登陆', 'data': 'cancel'}
        in_json = json.dumps(data).encode("hex")
        return Response(in_json)
