# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import requests
from django.conf import settings
from django.http import HttpResponse
from rest_framework import mixins, viewsets
from rest_framework import status
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from service.kernel.models.enterprise import EnterpriseUser
from service.kernel.tasks import send_verify_extras
from service.signature.models import Signature
from service.signature.serializers import SignatureSerializer


class SigninViewSet(NestedViewSetMixin, mixins.CreateModelMixin, GenericViewSet):
    '''
    用户登录接口.

    '''

    serializer_class = SignatureSerializer
    model = Signature

    def create(self, request, *args, **kwargs):
        # 测试数据
        # request = requests.get('http://10.7.7.22/media/verify_001.txt')
        # request.data = request.content

        # 验签数据
        resp = requests.post(settings.VERIFY_GATEWAY + '/Verify', data=request.data)

        if (resp.status_code != 200) and (resp.status_code != 500):
            third = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=resp.content)
            return HttpResponse(third.content)

        # 解析数据
        sign = resp.json()

        if sign.get('respCode') != '0000':
            print 'err'

        rest = json.loads(sign.get('source').decode('hex'))

        # 保存日志

        # 回调第三方然后返回给app
        enterprise = EnterpriseUser.objects.get(appkey=rest.get('data').get('appkey'))
        third = requests.post(url=enterprise.callback + rest['type'], data=request.data)

        if (third.status_code != 200) and (third.status_code != 500):
            third = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=third.content)
            return HttpResponse(third.content)

        # 服务签名
        third = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=third.content)
        return HttpResponse(third.content)


class SignupViewSet(viewsets.GenericViewSet):
    '''
    用户注册接口.

    '''
    serializer_class = SignatureSerializer
    model = Signature

    def create(self, request, *args, **kwargs):
        # 测试数据
        # request = requests.get('http://10.7.7.22/media/verify_001.txt')
        # request.data = request.content

        # 验签数据
        resp = requests.post(settings.VERIFY_GATEWAY + '/Verify', data=request.data)

        if (resp.status_code != 200) and (resp.status_code != 500):
            third = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=resp.content)
            return HttpResponse(third.content)

        # 解析数据
        sign = resp.json()
        if sign.get('respCode') != '0000':
            print 'err'

        rest = json.loads(sign.get('source').decode('hex'))

        # 保存日志

        # 回调第三方然后返回给app
        enterprise = EnterpriseUser.objects.get(appkey=rest.get('data').get('appkey'))
        third = requests.post(url=enterprise.callback + rest['type'], data=request.data)

        if (third.status_code != 200) and (third.status_code != 500):
            third = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=third.content)
            return HttpResponse(third.content)

        # 服务签名
        third = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=third.content)
        return HttpResponse(third.content)


class PaymentViewSet(viewsets.GenericViewSet):
    '''
    支付行为接口.

    '''
    serializer_class = SignatureSerializer
    model = Signature

    def create(self, request, *args, **kwargs):
        # 测试数据
        r = requests.get('http://10.7.7.22/media/verify_001.txt')
        request.data == r.content

        # request = open('verify_001.txt').read()

        # 验签数据
        resp = requests.post(settings.VERIFY_GATEWAY + '/Verify', data=request.data)

        if (resp.status_code != 200) and (resp.status_code != 500):
            third = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=resp.content)
            return HttpResponse(third.content)

        # 解析数据
        sign = resp.json()
        if sign.get('respCode') != '0000':
            print 'err'

        rest = json.loads(sign.get('source').decode('hex'))
        # 发送密文给银行
        bankrt = Bankserver(123)
        # 银行返回处理结果

        # 回调第三方然后返回给app
        third = requests.post(url=settings.PASSPORT + rest['type'], data=request.data)

        if (third.status_code != 200) and (third.status_code != 500):
            third = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=third.content)
            return HttpResponse(third.content)

        # 服务签名
        third = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=third.content)
        return HttpResponse(third.content)

    @list_route(methods=['GET', 'POST'])
    def validate(self, request, *args, **kwargs):
        a = send_verify_extras('HELLO', '[15010786971]', {'type': '1'})
        return Response(a, status=status.HTTP_200_OK)


class ReceiveViewSet(viewsets.GenericViewSet):
    '''
    收货行为接口.

    '''
    pass


class RefundsViewSet(viewsets.GenericViewSet):
    '''
    退货行为接口.

    '''
    pass


def Bankserver(message, *args, **kwargs):
    '''
    银行接口.

    '''
    return Response({'detail': '成功'}, status=status.HTTP_200_OK)

# def test():
#     '''
#     测试
#
#     '''
#     # data = {}
#     # data = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=json.dumps(data))
#     r = requests.get('http://10.7.7.22/media/verify_001.txt')
#     return requests.post('http://10.7.7.76:8000/api/passport/signin/', body=r.content)
