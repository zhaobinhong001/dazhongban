# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import sys

from service.trade.models import Purchased

reload(sys)
sys.setdefaultencoding("utf-8")
import arrow
import traceback
import logging
from rest_framework.authtoken.models import Token
import requests
from django.conf import settings
from django.http import HttpResponse
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from service.consumer.models import Notice
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
        # 服务验签

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
        # 服务签名

        resp = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=data)

        if resp.status_code != 200:
            sign = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=resp.content)
            return sign.content

        return resp.content

    def third(self, type='signin', data=None):
        # 服务第三方

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
        # 发送 push
        # 保存记录入库

        try:
            notice = Notice(**kwargs)
            notice.save()
        except Exception as e:
            raise e

    def signa(self, text=None, owner=None, rest=None):
        kwargs = {
            'owner': owner,
            'type': rest['type'],
            'extra': json.dumps(rest),
            'signs': text,
            'serial': text['serialNo'],
            'expired': arrow.get(text['endDate']).format('YYYY-MM-DD')
        }

        try:
            s = Signature(**kwargs)
            s.save()
            return 'ok'
        except Exception as e:
            return e.message

    def owner(self, appkey=None, openid=None, token=None):

        try:
            if not token:
                log = WaterLog.objects.filter(appkey=appkey, openid=openid).get()
                return log.owner
            else:
                obj = Token.objects.get(key=token)
                return obj.user
        except WaterLog.DoesNotExist:
            return False


class SigninViewSet(NestedViewSetMixin, mixins.CreateModelMixin, GenericViewSet, BaseViewSet):
    '''
    用户登陆接口.

    '''
    serializer_class = SignatureSerializer
    model = Signature
    parser_classes = (StreamParser,)

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

        # 推送消息
        message = json.loads(third)
        kwargs = {'subject': message['detail'], 'content': message['detail'], 'owner': owner, 'extra': message,
                  'type': 'signin'}

        self.notice(**kwargs)

        # 写入日志
        sg = self.signa(text, owner, rest)
        third = sg if sg != 'ok' else third

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

        # 推送消息
        message = json.loads(third)
        kwargs = {'subject': message['detail'], 'content': message['detail'], 'owner': owner, 'extra': message,
                  'type': 'signup'}

        self.notice(**kwargs)

        # 写入日志
        sg = self.signa(text, owner, rest)
        third = sg if sg != 'ok' else third

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
        try:
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

            record = {
                'owner': owner,
                'type': rest['type'],
                'extra': rest,
                'signs': text,
                'serial': text['serialNo'],
                'expired': arrow.get(text['endDate']).format('YYYY-MM-DD')
            }

            signature = Signature(**record)
            signature.save()

            # 保存消费记录
            kwargs1 = {
                'owner': owner,
                'signa': signature,
                'type': rest['type'],
                'title': rest['data']['goods']['title'],
                'amount': rest['data']['goods']['amount'],
                'bank_accountName': '建设银行',
                'payment': '621000000000000',
                'receipt': '621111111111111',
                'account': '大排档',
                'consumer': '小龙虾',
            }
            purchased = Purchased(**kwargs1)
            purchased.save()

        # except Exception as e:
        #     third = e.message
        except Exception:
            s = traceback.format_exc()
            third = s

        # 写入日志
        # sg = self.signa(text, owner, rest)
        # third = sg if sg != 'ok' else third
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
        try:
            # 回调第三方然后返回给app
            third = self.third(type=rest['type'], data=self.sign(data=json.dumps(rest)).decode('hex'))

            # @todo 推送消息

            owner = self.owner(rest['data']['appkey'], rest['data']['openid'])
            message = json.loads(third)
            kwargs = {'subject': message['detail'], 'content': message['detail'], 'owner': owner, 'extra': message,
                      'type': 'receive'}

            self.notice(**kwargs)
        except Exception as e:
            third = e.message

        # 写入日志
        sg = self.signa(text, owner, rest)
        third = sg if sg != 'ok' else third

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
        try:
            # 回调第三方然后返回给app
            third = self.third(type=rest['type'], data=self.sign(data=json.dumps(rest)).decode('hex'))

            # @todo 推送消息
            owner = self.owner(rest['data']['appkey'], rest['data']['openid'])
            message = json.loads(third)
            kwargs = {'subject': message['detail'], 'content': message['detail'], 'owner': owner, 'extra': message,
                      'type': 'refunds'}
            self.notice(**kwargs)

        # 服务签名
        except Exception as e:
            third = e.message

        # 写入日志
        sg = self.signa(text, owner, rest)
        third = sg if sg != 'ok' else third
        return HttpResponse(self.sign(third))


class PushViewSet(viewsets.GenericViewSet, BaseViewSet):
    '''
    推送接口.

    '''

    def create(self, request, *args, **kwargs):

        extras = request.data
        owner = self.owner(extras.get('data').get('appkey'), extras.get('data').get('openid'))
        kwargs = {
            'subject': settings.NOTICE_TYPE_MSGS.get(extras['type']),
            'content': settings.NOTICE_TYPE_MSGS.get(extras['type']),
            'owner': owner,
            'extra': extras,
            'type': extras['type']
        }

        try:
            self.notice(**kwargs)
            content = {'errors': 0, 'detail': '推送成功'}
        except Exception as e:
            content = {'errors': 1, 'detail': '推送失败'}

        return Response(content)
