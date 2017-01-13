# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
from django.http import HttpResponse
from rest_framework import viewsets

import json
from django.conf import settings


class SigninViewSet(viewsets.GenericViewSet):
    '''
    用户登录接口.

    '''

    # def create(self, request, *args, **kwargs):
    pass


class SignupViewSet(viewsets.GenericViewSet):
    '''
    用户注册接口.

    '''
    pass
    # def create(self, request, *args, **kwargs):
    #     pass
    #     # 接受并验签数据
    #     resp = requests.post(settings.VERIFY_GATEWAY + '/Verify', data=request.body)
    #     # 解析数据
    #     sign = resp.json()
    #     rest = json.loads(sign.get('source').decode('hex'))
    #     # 处理数据
    #
    #     # 服务签名并返回
    #     resp = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=rest)
    #     return HttpResponse(resp.content)


class PaymentViewSet(viewsets.GenericViewSet):
    '''
    支付行为接口.

    '''
    pass
    # 接受并验签数据
    # 解析数据
    # 发送密文给银行
    # 银行返回处理结果
    # 处理数据
    # 服务签名并返回


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
