# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import requests
from django.conf import settings
from django.http import HttpResponse
from rest_framework import mixins, viewsets
from rest_framework.viewsets import GenericViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from service.kernel.models.enterprise import EnterpriseUser
from service.kernel.utils.jpush_audience import jpush_extras
from service.signature.models import Signature
from service.signature.serializers import SignatureSerializer


class StreamParser(object):
    """
    All parsers should extend `BaseParser`, specifying a `media_type`
    attribute, and overriding the `.parse()` method.
    """
    media_type = '*/*'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Given a stream to read from, return the parsed representation.
        Should return parsed data, or a `DataAndFiles` object consisting of the
        parsed data and files.
        """
        return stream


class SigninViewSet(NestedViewSetMixin, mixins.CreateModelMixin, GenericViewSet):
    '''
    用户登录接口.

    '''

    serializer_class = SignatureSerializer
    model = Signature
    parser_classes = (StreamParser,)

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
    parser_classes = (StreamParser,)
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
    parser_classes = (StreamParser,)

    def create(self, request, *args, **kwargs):
        # 验签数据
        resp = requests.post(settings.VERIFY_GATEWAY + '/Verify', data=request.data)

        if (resp.status_code != 200) and (resp.status_code != 500):
            third = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=resp.content)
            return HttpResponse(third.content)

        # 解析数据
        sign = resp.json()
        source = sign.get('source').decode('hex')
        rest = json.loads(source)

        # return HttpResponse(resp.content)

        # 回调第三方然后返回给app
        # third = requests.post(url=settings.PASSPORT + rest['type'], data=request.data)
        # third = object
        # content = third.content

        # if (third.status_code != 200) and (third.status_code != 500):
        #     third = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=third.content)
        #     return HttpResponse(third.content)

        # 服务签名
        content = json.dumps({'errors': 1, 'detail': '异常错误'})
        third = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=content)
        return HttpResponse(third.content)


class ReceiveViewSet(viewsets.GenericViewSet):
    '''
    收货行为接口.

    '''
    parser_classes = (StreamParser,)

    def create(self, request, *args, **kwargs):
        # 验签数据
        resp = requests.post(settings.VERIFY_GATEWAY + '/Verify', data=request.data)

        if (resp.status_code != 200) and (resp.status_code != 500):
            third = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=resp.content)
            return HttpResponse(third.content)

        # 解析数据
        sign = resp.json()
        source = sign.get('source').decode('hex')
        rest = json.loads(source)

        # 回调第三方然后返回给app
        # third = requests.post(url=settings.PASSPORT + rest['type'], data=request.data)
        # third = object
        # content = third.content

        # if (third.status_code != 200) and (third.status_code != 500):
        #     third = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=third.content)
        #     return HttpResponse(third.content)

        # 服务签名
        content = json.dumps({'errors': 1, 'detail': '异常错误'})
        third = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=content)
        return HttpResponse(third.content)


class RefundsViewSet(viewsets.GenericViewSet):
    '''
    退货行为接口.

    '''
    parser_classes = (StreamParser,)

    def create(self, request, *args, **kwargs):
        # 验签数据
        resp = requests.post(settings.VERIFY_GATEWAY + '/Verify', data=request.data)

        if (resp.status_code != 200) and (resp.status_code != 500):
            third = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=resp.content)
            return HttpResponse(third.content)

        # 解析数据
        sign = resp.json()
        source = sign.get('source').decode('hex')
        rest = json.loads(source)

        # 回调第三方然后返回给app
        # third = requests.post(url=settings.PASSPORT + rest['type'], data=request.data)
        # third = object
        # content = third.content

        # if (third.status_code != 200) and (third.status_code != 500):
        #     third = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=third.content)
        #     return HttpResponse(third.content)

        # 服务签名
        content = json.dumps({'errors': 1, 'detail': '异常错误'})
        third = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=content)
        return HttpResponse(third.content)


from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView


class PushView(APIView):
    """
    A view that can accept POST requests with JSON content.
    """
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        push = jpush_extras(message='hello', alias=['15711412157'], extras=json.loads(request.data))
        content = json.dumps({'errors': 0, 'detail': '发送成功'})
        return Response(json.loads(request.data))


class PushViewSet(viewsets.GenericViewSet):
    parser_classes = (StreamParser,)

    def create(self, request, *args, **kwargs):
        # try:
        extras = {
            'type': 'receive',
            'data': {
                'req_id': '请求唯一的id, 发起方随机生成',
                'appkey': '系统分配给商家的唯一标示',
                'uri': '/api/passport/receive/',
                'orders': {
                    'goods': {
                        'title': '',
                        'amount': '',
                        'quantity': '',
                    },
                    'users': {
                        'name': '',
                        'mobile': '',
                        'address': '',
                    },
                    'orderid': '',
                    'created': '',
                    'fee': '',
                    'discount': '',
                    'paymend': '',
                }
            }
        }

        # extras = json.loads(str(request.data))
        # print request.data
        # push = jpush_extras(message='hello', alias=['15711412157'], extras=extras)
        # content = json.dumps({'errors': 0, 'detail': '发送成功'})
        # except Exception:
        #     content = json.dumps({'errors': 1, 'detail': '异常错误'})
        # data = request.data

        # print (request.data)



        return Response(request.data)
