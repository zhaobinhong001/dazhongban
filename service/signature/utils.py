# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import requests as req
from django.conf import settings

from service.consumer.utils import md5

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

IDDENTITY_APPKEY = settings.IDDENTITY_APPKEY
IDDENTITY_GATEWAY = settings.IDDENTITY_GATEWAY

fields = data['data'].keys()


def iddentity_verify(param=None):
    if param is None:
        return False

    data = {'data': {"certType": "1", "originType": "12"}}

    data['data'].update(param)
    data['signKey'] = md5('%s%s%s' % (data['data']['certId'], data['data']['phone'], IDDENTITY_APPKEY))
    data['signKey'] = data['signKey'].hexdigest()

    data = json.dumps(data)
    headers = {'content-type': 'application/json; charset=utf-8'}
    ret = req.post(url=IDDENTITY_GATEWAY, data=data, headers=headers, verify=False)

    if ret.status_code == 200:
        item = ret.json()
        item['cardNo'] = param['cardNo']
        return item

    return False
