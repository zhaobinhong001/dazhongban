# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import requests as req

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

IDDENTITY_APPKEY = '69tx91g3kpzlqkndszzofj38fr'
IDDENTITY_GATEWAY = 'https://10.7.7.71:3002/api/register'

fields = data['data'].keys()


def iddentity_verify(param=None):
    if param is None:
        return False

    data = {'data': {"certType": "1", "originType": "12"}}

    data['data'].update(param)
    data['signKey'] = md5('%s%s%s' % (data['data']['certId'], data['data']['phone'], IDDENTITY_APPKEY))
    data['signKey'] = data['signKey'].hexdigest()

    data = json.dumps(data)
    ret = req.post(url=IDDENTITY_GATEWAY, data=data, headers={'content-type': 'application/json; charset=utf-8'},
        verify=False)

    if ret.status_code == 200:
        return ret.json()

    return False
