# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import requests as req
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from service.consumer.utils import md5
from service.trade.models import Contract

data = {
    "data": {
        "certId": "411527199208117052",
        "certType": "1",
        "name": "刘春雷",
        "phone": "18637638958",
        "originType": "12",
        "address": "",
        "frontPhoto": "",
        "backPhoto": "",
        "cvn2": "",
        "cardNo": "6217000010077471293",
        "bankID": "105",
        "exp_Date": ""
    },
    "signKey": "4199bdf5ed7fc0fdc436b2a7480b4092"
}

APPKEY = settings.IDDENTITY_APPKEY
GATEWAY = settings.IDDENTITY_GATEWAY

fields = data['data'].keys()


def iddentity_verify(param=None):
    if param is None:
        return '参数错误', False
    try:
        del param['certType']
        del param['originType']
    except Exception as e:
        pass

    data = {'data': {"certType": "1", "originType": "12"}}
    data['data'].update(param)
    data['signKey'] = md5('%s%s%s' % (data['data']['certId'], data['data']['phone'], APPKEY)).hexdigest()
    headers = {'content-type': 'application/json; charset=utf-8', 'accept': 'application/json'}

    ret = req.post(url=GATEWAY, data=json.dumps(data), headers=headers, verify=False)

    if ret.status_code == 200:
        item = ret.json()
        item['cardNo'] = param['cardNo']
        return item, True

    return u'认证服务器错误' + ret.content, False


def process_verify(uri, data):
    try:
        token = Token.objects.filter(key=data.get('token')).get()
        del data['token']
    except Token.DoesNotExist:
        return {'errors': 1, 'detail': '用户不存在'}, False

    if '/contract/' in uri:
        if data.get('id'):
            try:
                res = Contract.objects.get(id=data.get('id'))
                res.receiver = token.user
                del data['id']
            except Contract.DoesNotExist:
                return {'errors': 1, 'detail': '合约不存在'}, False
        else:
            res = Contract()
            res.sender_id = token.user.pk

        for key, val in data.items():
            if hasattr(res, key):
                setattr(res, key, val)

        res.save()

    elif '/transfer/' in uri:

        type = data.get('type')
        status = data.get('status')

        if not type:
            return {'errors': 1, 'detail': 'type 不能为空'}, False

        if not status:
            return {'errors': 1, 'detail': 'status 不能为空'}, False

        # 转账时收款方不能为空
        if data.get('type') != 'receiver':
            if data.get('receiver_id'):
                try:
                    receiver = get_user_model().objects.get(id=data.get('receiver_id'))
                    receiver_id = receiver.pk
                except get_user_model().DoesNotExist:
                    return {'errors': 1, 'detail': '收款方不存在'}, False
            else:
                return {'errors': 1, 'detail': '收款方不能为空'}, False

        if data.get('id'):
            try:
                res = Contract.objects.get(id=data.get('id'))
                res.receiver = token.user
                del data['id']
            except Contract.DoesNotExist:
                return {'errors': 1, 'detail': '交易订单不存在'}, False
        else:
            res = Contract()

            if type == 'transfer':
                res.sender_id = token.user.pk
                res.receiver_id = receiver_id
            elif type == 'receiver':
                res.sender_id = token.user.pk
            elif type == 'thirty':
                pass

        for key, val in data.items():
            if hasattr(res, key):
                setattr(res, key, val)

        res.save()

    return {'errors': 0,
        'detail': {'type': res.type, 'data': {'status': res.status, 'uri': uri, 'id': res.id}}}, token.user
