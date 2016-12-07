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
        "originType": "1",
        "address": "",
        "frontPhoto": "",
        "backPhoto": "",
        "cvn2": "",
        "cardNo": "6217000010077471293",
        "bankID": "CCB",
        "exp_Date": ""
    },
    "signKey": "8b347d22257c6092821798f811bce0a1"
}


def iddentity_verify(data=None):
    if data is None:
        return False

    url = 'https://121.42.154.8:3002/api/register'
    data['signKey'] = md5('%s%s%s' % (data['data']['certId'], data['data']['phone'], 'l53sevsz8bt4om3hqe6rbe29'))
    data['signKey'] = data['signKey'].hexdigest()
    data = json.dumps(data)
    ret = req.post(url=url, data=data, headers={'content-type': 'application/json; charset=utf-8'}, verify=False)

    if ret.status_code == 200:
        return ret.json()

    return False
