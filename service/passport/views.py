# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import sys

from rest_framework.permissions import IsAuthenticated

from service.consumer.serializers import UserSerializer

reload(sys)
sys.setdefaultencoding("utf-8")
from rest_framework.authtoken.models import Token
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

from service.consumer.models import Notice
from service.kernel.models.enterprise import EnterpriseUser
from service.kernel.utils.jpush_audience import jpush_extras
from service.passport.models import WaterLog
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


class BaseViewSet(object):
    def verify(self, data=''):
        resp = requests.post(settings.VERIFY_GATEWAY + '/Verify', data=data)
        errors = False

        if (resp.status_code != 200) and (resp.status_code != 500):
            errors = True

        text = resp.json()

        if text.get('respCode') != '0000':
            errors = True

        if errors:
            sign = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=resp.content)
            return sign.content, False

        return text, True

    def sign(self, data=''):
        resp = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=data)

        if resp.status_code != 200:
            sign = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=resp.content)
            return sign.content

        return resp.content

    def third(self, type='signin', data=None):
        try:
            third = requests.post(url=settings.PASSPORT + '/services/callback/%s' % type, data=data)
            return third.content
        except requests.ConnectTimeout:
            return self.sign(json.dumps({'errors': 1, 'detail': u'连接超时'}))
        except requests.ConnectionError:
            return self.sign(json.dumps({'errors': 1, 'detail': u'连接错误'}))
        except Exception:
            pass

    def source(self, data):
        try:
            rest = json.loads(data.get('source').decode('hex').decode('hex'))
        except Exception:
            rest = json.loads(data.get('source').decode('hex'))

        return rest

    def notice(self, **kwargs):
        print 'notice staring...'
        # 发送 push
        # 保存记录入库
        # try:
        notice = Notice(**kwargs)
        notice.save()

        print 'notice done'

    def owner(self, appkey=None, openid=None, token=None):
        try:
            if not token:
                log = WaterLog.objects.filter(appkey=appkey, openid=openid).get()
                return log.owner
            else:
                obj = Token.objects.get(token=token)
                return obj.user
        except WaterLog.DoesNotExist:
            return False


class SigninViewSet(NestedViewSetMixin, mixins.CreateModelMixin, GenericViewSet, BaseViewSet):
    '''
    用户登录接口.

    {
        'type':'payment', // action 详见 APP 接口表
        'data': {
            'req_id': '请求唯一的id, 发起方随机生成'
            'appkey': 'val',                  // 系统分配给商家的唯一标示
            'uri': '/api/passport/payment/'  // APP 服务器的 uri 路径
            'orderid': '',        // 订单号码
        }
    }

    '''

    serializer_class = SignatureSerializer
    model = Signature
    # permission_classes = (IsAuthenticated,)
    parser_classes = (StreamParser,)

    def create(self, request, *args, **kwargs):
        # 验签数据
        text, status = self.verify(request.data)

        if not status:
            return HttpResponse(text)

        # 解析数据
        rest = self.source(text)

        # @todo 保存日志

        # 回调第三方然后返回给app
        third = self.third(type=rest['type'], data=self.sign(data=json.dumps(rest)).decode('hex'))

        # @todo 推送消息

        # 服务签名
        return HttpResponse(self.sign(third))


class SignupViewSet(viewsets.GenericViewSet, BaseViewSet):
    '''
    用户注册接口.

    '''
    serializer_class = SignatureSerializer
    parser_classes = (StreamParser,)
    model = Signature

    def create(self, request, *args, **kwargs):
        # 验签数据
        text, status = self.verify(request.data)

        if not status:
            return HttpResponse(text)

        # 解析数据
        rest = self.source(text)

        # 保存日志
        # --------------------------
        owner = self.owner(token=rest.get('data').get('token'))
        log, _ = WaterLog.objects.get_or_create(appkey=rest.get('data').get('appkey'), owner=owner)
        log.save()

        rest['data']['openid'] = log.openid
        # ----------------------------------

        # 回调第三方然后返回给app
        third = self.third(type=rest['type'], data=self.sign(data=json.dumps(rest)).decode('hex'))

        # @todo 推送消息

        # 服务签名
        return HttpResponse(self.sign(third))


class PaymentViewSet(viewsets.GenericViewSet, BaseViewSet):
    '''
    支付行为接口.

    '''
    serializer_class = SignatureSerializer
    parser_classes = (StreamParser,)

    def create(self, request, *args, **kwargs):
        # 验签数据
        text, status = self.verify(request.data)
        if not status:
            return HttpResponse(text)

        # 解析数据
        rest = self.source(text)

        # 调用银行接口
        payment = requests.post(url=settings.PAYMENT_INTEFACE + '/services/payment/',
                                data=self.sign(data=json.dumps(rest)).decode('hex'))

        # 回调第三方然后返回给app
        third = self.third(type=rest['type'], data=payment.content)

        # @todo 保存记录

        # 推送消息
        owner = self.owner(rest['data']['appkey'], rest['data']['openid'])
        message = json.loads(third)
        kwargs = {'subject': message['detail'], 'content': message['detail'], 'owner': owner, 'extra': message,
                  'type': 'payment'}

        self.notice(**kwargs)

        # 服务签名
        return HttpResponse(self.sign(third))


class ReceiveViewSet(viewsets.GenericViewSet, BaseViewSet):
    '''
    收货行为接口.

    '''
    parser_classes = (StreamParser,)

    def create(self, request, *args, **kwargs):
        # 验签数据
        text, status = self.verify(request.data)
        if not status:
            return HttpResponse(text)

        # 解析数据
        rest = self.source(text)

        # @todo 保存日志

        # 回调第三方然后返回给app
        third = self.third(type=rest['type'], data=self.sign(data=json.dumps(rest)).decode('hex'))

        # @todo 推送消息

        owner = self.owner(rest['data']['appkey'], rest['data']['openid'])
        message = json.loads(third)
        kwargs = {'subject': message['detail'], 'content': message['detail'], 'owner': owner, 'extra': message,
                  'type': 'receive'}

        self.notice(**kwargs)

        # 服务签名
        return HttpResponse(self.sign(third))


class RefundsViewSet(viewsets.GenericViewSet, BaseViewSet):
    '''
    退货行为接口.

    '''
    parser_classes = (StreamParser,)

    def create(self, request, *args, **kwargs):
        # 验签数据
        text, status = self.verify(request.data)

        if not status:
            return HttpResponse(text)

        # 解析数据
        rest = self.source(text)

        # @todo 保存日志

        # 回调第三方然后返回给app
        third = self.third(type=rest['type'], data=self.sign(data=json.dumps(rest)).decode('hex'))

        # @todo 推送消息
        owner = self.owner(rest['data']['appkey'], rest['data']['openid'])
        message = json.loads(third)
        kwargs = {'subject': message['detail'], 'content': message['detail'], 'owner': owner, 'extra': message,
                  'type': 'refunds'}
        self.notice(**kwargs)

        # 服务签名
        return HttpResponse(self.sign(third))


class PushViewSet(viewsets.GenericViewSet):
    def create(self, request, *args, **kwargs):
        extras = request.data
        owner = self.owner(extras['data']['appkey'], extras['data']['openid'])
        kwargs = {'subject': extras['data']['req_id'], 'content': extras['data']['req_id'], 'owner': owner,
                  'extra': extras,
                  'type': extras['type']}

        try:
            self.notice(**kwargs)
            content = {'errors': 0, 'detail': '推送成功'}
        except Exception as e:
            content = {'errors': 1, 'detail': '推送失败'}

        return Response(content)
