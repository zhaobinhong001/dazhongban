# -*- coding: utf-8 -*-
# Create your tasks here
from __future__ import absolute_import, unicode_literals
import requests as req
import time
from celery import shared_task


@shared_task
def add(x, y):
    time.sleep(50000)
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


# @shared_task
# def dxfxcs(mobile, content):
#     payload = {'action': 'send', 'userid': '4823', 'account': 'K000319', 'password': '065329', 'mobile': mobile,
#                'content': "短信验证码" + content + "【收付宝科技】", 'sendTime': '', 'taskName': '', 'checkcontent': '1',
#                'mobilenumber': '1',
#                'countnumber': '1', 'telephonenumber': '0'}
#
#     r = req.get("http://xtx.telhk.cn:8888/sms.aspx", params=payload)
#
#     print (r.content)


def send_sms(mobile, message, *args, **kwargs):
    return True

usernae =''
nickname =''
message = '%(username)s'

send_sms(mobile='mobile', message='ssdfsd{}fds')