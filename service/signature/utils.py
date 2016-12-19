# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import requests as req
from django.conf import settings
from django.contrib.auth import get_user_model

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
        open('iddentity_result.txt', 'w').write(ret.content)
        item = ret.json()
        item['cardNo'] = param['cardNo']
        open('iddentity_input.txt', 'w').write(json.dumps(item))
        return item, True

    return '认证服务器错误' + ret.content, False


def process_verify(uri, data, request):
    receiver = get_user_model().objects.filter(mobile=data.get('mobile'))

    if not receiver:
        return False

    if '/contract/' in uri:
        if data.get('id'):
            res = Contract.objects.get(id=data.get('id'))
            del data['id']
        else:
            res = Contract()
            res.sender_id = 1

        for key, val in data.items():
            if hasattr(res, key):
                setattr(res, key, val)

        res.receiver = receiver
        res.save()

    elif '/transfer/' in uri:
        if data.get('id'):
            res = Transfer.objects.get(id=data.get('id'))
            del data['id']
        else:
            res = Transfer()
            res.sender_id = 1

        for key, val in data.items():
            if hasattr(res, key):
                setattr(res, key, val)

        res.receiver = receiver
        res.save()

    return {'detail': '操作成功'}, True
