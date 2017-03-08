# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


def contrtem(type, data, **kwargs):
    '''
    合约模板

    '''
    data = data.update(kwargs)

    content = {}

    content['receipt'] = "今日本人向 %(borrower)s (身份证号码: %(identity)s)借款人民币 %(amount)f元(大写:XXX)立此为据"
    content['borrow'] = "今日本人向 %(borrower)s (身份证号码: %(identity)s)借款人民币 %(amount)f元(大写:XXX)立此为据"
    content['owe'] = "今日本人向 %(borrower)s (身份证号码: %(identity)s)借款人民币 %(amount)f元(大写:XXX)立此为据"
    content['signin'] = "登陆成功"
    content['signup'] = "注册成功"

    return content[type] % data
