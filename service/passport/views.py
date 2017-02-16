# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import requests
from django.conf import settings
from django.http import HttpResponse
from rest_framework import mixins, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.request import Request
from django.http.request import HttpRequest
from rest_framework.views import APIView
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

        # 验签数据
        resp = requests.post(settings.VERIFY_GATEWAY + '/Verify', data=request.data)

        if (resp.status_code != 200) and (resp.status_code != 500):
            third = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=resp.content)
            return HttpResponse(third.content)

        # 解析数据
        sign = resp.json()

        if sign.get('respCode') != '0000':
            return HttpResponse(sign.get('respMsg'))

        try:
            rest = json.loads(sign.get('source').decode('hex').decode('hex'))
        except Exception:
            rest = json.loads(sign.get('source').decode('hex'))

        # 保存日志

        # 回调第三方然后返回给app
        data = json.dumps(rest)
        data = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=data)
        data = data.content.decode('hex')
        try:
            third = requests.post(url=settings.PASSPORT + '/services/callback/' + rest['type'], data=data)
        except Exception:
            return HttpResponse(third.content)

        if (third.status_code != 200) and (third.status_code != 500):
            third = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=third.content)
            return HttpResponse(third.content)
            #
            # @todo 推送消息
            # Notice.objects.all()

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
            return HttpResponse(sign.get('respMsg'))

        try:
            rest = json.loads(sign.get('source').decode('hex').decode('hex'))
        except Exception:
            rest = json.loads(sign.get('source').decode('hex'))

        # 保存日志

        # 回调第三方然后返回给app
        data = json.dumps(rest)
        data = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=data)
        data = data.content.decode('hex')

        try:
            third = requests.post(url=settings.PASSPORT + '/services/callback/' + rest['type'], data=data)
        except Exception:
            return HttpResponse(third.content)

        if (third.status_code != 200) and (third.status_code != 500):
            third = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=third.content)
            return HttpResponse(third.content)

        # @todo 推送消息

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
            return HttpResponse(sign.get('respMsg'))

        try:
            rest = json.loads(sign.get('source').decode('hex').decode('hex'))
        except Exception:
            rest = json.loads(sign.get('source').decode('hex'))

        data = json.dumps(rest)
        data = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=data)
        data = data.content.decode('hex')
        # 调用银行接口
        try:
            payment = requests.post(url=settings.PAYMENT_INTEFACE + '/services/payment/', data=data)
        except Exception:
            return HttpResponse(payment.content)

        # 回调第三方然后返回给app
        try:
            third = requests.post(url=settings.PASSPORT + '/services/callback/' + rest['type'],
                                  data=payment.content)
        except Exception:
            return HttpResponse(third.content)

        if (third.status_code != 200) and (third.status_code != 500):
            third = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=third.content)
            return HttpResponse(third.content)

        # 服务签名
        # content = json.dumps({'errors': 0, 'detail': '支付成功'})
        # @todo 推送消息
        # PushView()

        third = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=third.content)
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
        if sign.get('respCode') != '0000':
            return HttpResponse(sign.get('respMsg'))

        try:
            rest = json.loads(sign.get('source').decode('hex').decode('hex'))
        except Exception:
            rest = json.loads(sign.get('source').decode('hex'))

        # 保存日志

        # 回调第三方然后返回给app
        data = json.dumps(rest)
        data = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=data)
        data = data.content.decode('hex')

        try:
            third = requests.post(url=settings.PASSPORT + '/services/callback/' + rest['type'], data=data)
        except Exception:
            return HttpResponse(third.content)

        if (third.status_code != 200) and (third.status_code != 500):
            third = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=third.content)
            return HttpResponse(third.content)

        # # @todo 推送消息
        # PushView(third.content)
        # 服务签名
        # third = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=third.content)
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
        if sign.get('respCode') != '0000':
            return HttpResponse(sign.get('respMsg'))

        try:
            rest = json.loads(sign.get('source').decode('hex').decode('hex'))
        except Exception:
            rest = json.loads(sign.get('source').decode('hex'))

        # 保存日志

        # 回调第三方然后返回给app
        data = json.dumps(rest)
        data = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=data)
        data = data.content.decode('hex')

        try:
            third = requests.post(url=settings.PASSPORT + '/services/callback/' + rest['type'], data=data)
        except Exception:
            return HttpResponse(third.content)

        if (third.status_code != 200) and (third.status_code != 500):
            third = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=third.content)
            return HttpResponse(third.content)

        # @todo 推送消息
        
        # 服务签名
        third = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=third.content)
        return HttpResponse(third.content)


class PushView(APIView):
    """
    A view that can accept POST requests with JSON content.
    """
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        jpush_extras(message='hello', alias=['15711412157', '18511345772', '15010786971'],
                     extras={'errors': 0, 'detail': {'errors': 0, 'detail': '支付成功'}})
        # jpush_extras(message='hello', alias=['15711412157', '18511345772', '15010786971'],
        #              extras={'errors': 0, 'detail': json.loads(request.data)})
        content = json.dumps({'errors': 0, 'detail': '发送成功'})
        return Response(content)


class PushViewSet(viewsets.GenericViewSet):
    parser_classes = (StreamParser,)

    def create(self, request, *args, **kwargs):
        # try:
        # extras = {
        #     'type': 'receive',
        #     'data': {
        #         'req_id': '请求唯一的id, 发起方随机生成',
        #         'appkey': '系统分配给商家的唯一标示',
        #         'uri': '/api/passport/receive/',
        #         'orders': {
        #             'goods': {
        #                 'title': '',
        #                 'amount': '',
        #                 'quantity': '',
        #             },
        #             'users': {
        #                 'name': '',
        #                 'mobile': '',
        #                 'address': '',
        #             },
        #             'orderid': '',
        #             'created': '',
        #             'fee': '',
        #             'discount': '',
        #             'paymend': '',
        #         }
        #     }
        # }

        extras = json.loads(str(request.data))

        push = jpush_extras(message='hello', alias=['15711412157'], extras=extras)
        data = request.data

        return Response(data)
