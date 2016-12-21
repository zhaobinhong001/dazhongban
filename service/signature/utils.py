# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import requests as req
from django.conf import settings
from rest_framework.authtoken.models import Token

from service.consumer.utils import md5
from service.trade.models import Contract, Transfer

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
    print ret.content

    if ret.status_code == 200:
        item = ret.json()
        item['cardNo'] = param['cardNo']
        return item, True

    return '认证服务器错误' + ret.content, False


def process_verify(uri, data):
    try:
        token = Token.objects.filter(key=data.get('token')).get()
    except Token.DoesNotExist:
        return {'errors': 1, 'detail': '用户不存在'}

    if data.get('token'):
        del data['token']

    if '/contract/' in uri:
        if data.get('id'):
            try:
                res = Contract.objects.get(id=data.get('id'))
                res.receiver = token.user
                del data['id']
            except Contract.DoesNotExist:
                return {'errors': 1, 'detail': '合约不存在'}
        else:
            res = Contract()
            res.sender_id = token.user.pk

        for key, val in data.items():
            if hasattr(res, key):
                setattr(res, key, val)

        res.save()

    elif '/transfer/' in uri:
        if data.get('id'):
            try:
                res = Transfer.objects.get(id=data.get('id'))
                res.receiver = token.user
                del data['id']
            except Transfer.DoesNotExist:
                return {'errors': 1, 'detail': '交易订单不存在'}
        else:
            res = Transfer()
            res.sender_id = token.user.pk

        for key, val in data.items():
            if hasattr(res, key):
                setattr(res, key, val)

        res.save()

    return {'errors': 0, 'detail': {'uri': uri, 'id': res.id}}
