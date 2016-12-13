# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests

from service.restauth.models import VerifyCode


def send_sms(mobile, message, *args, **kwargs):
    url = "http://xtx.telhk.cn:8888/sms.aspx"
    payload = {
        'action': 'send',
        'userid': '4823',
        'account': 'K000319',
        'password': '065329',
        'mobile': mobile,
        'content': message,
        'sendTime': '',
        'taskName': '',
        'checkcontent': '1',
        'mobilenumber': '1',
        'countnumber': '1',
        'telephonenumber': '0'
    }

    r = requests.post(url=url, data=payload)
    return u'Success' in r.content


def check_verify_code(mobile, verify):
    result = VerifyCode.objects.filter(mobile=mobile, code=verify).exists()
    VerifyCode.objects.filter(mobile=mobile, code=verify).delete() if result else None
    return True if result else False
