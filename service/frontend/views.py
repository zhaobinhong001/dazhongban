# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from cStringIO import StringIO

import datetime
import qrcode
import short_url
import time
from django.http import HttpResponse
from django.shortcuts import render
from service.frontend.models import QRToken


def generate_qrcode(data, size=11):
    qr = qrcode.QRCode(version=1, box_size=size, border=1, error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(data)
    qr.make(fit=True)
    im = qr.make_image()

    return im


def q(request, uid):
    uid = short_url.decode_url(uid)
    url = 'http://' + request.get_host() + '/api/users/%s/invite/' % uid
    img = generate_qrcode(url)
    buf = StringIO()
    img.save(buf)

    stream = buf.getvalue()
    return HttpResponse(stream, content_type="image/jpeg")


def qs(request, key):
    # 生成扫码登陆图片

    try:
        token = QRToken.objects.filter(key=key).get()
        img = generate_qrcode(token.raw)
        buf = StringIO()
        img.save(buf)

        stream = buf.getvalue()
        return HttpResponse(stream, content_type="image/jpeg")
    except QRToken.DoesNotExist:
        # 不存在提示
        return HttpResponse('key 参数错误')


def scan_login(request):
    # 生成token
    token = QRToken()

    # 生成url
    done = 'http://' + request.get_host() + '/api/qrlogin/%s/done/' % token.key
    scan = 'http://' + request.get_host() + '/api/qrlogin/%s/scan/' % token.key
    cancel = 'http://' + request.get_host() + '/api/qrlogin/%s/cancel/' % token.key
    check = 'http://' + request.get_host() + '/api/qrlogin/%s/check/' % token.key

    # 写入数据库
    token.raw = {'type': 'qrlogin', 'data': json.dumps({'done': done, 'scan': scan, 'cancel': cancel}).encode('hex')}
    token.save()

    key = token.key

    return render(request, 'scanlogin.html', locals())

# def check(request, key):
#     # 查看扫码状态
#     obj = QRToken.objects.filter(key=key).get()
#     nowTime = int(time.mktime(datetime.datetime.now().timetuple()))
#     created = int(time.mktime(obj.created.timetuple()))
#     isexpiration = nowTime - created
#
#     try:
#         if isexpiration > 60:
#             return HttpResponse('408')
#         elif obj.owner is None:
#             return HttpResponse('505')
#         else:
#             return HttpResponse('201')
#     except QRToken.DoesNotExist:
#         raise Exception()
#
#
# def success(request):
#     # 登陆成功返回的页面
#     return render(request, 'success.html')
#
#
# def expiration(request):
#     # 登陆超时返回的页面
#     return render(request, 'expiration.html')
