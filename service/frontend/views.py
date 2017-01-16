# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import tempfile
from cStringIO import StringIO
from random import choice

import qrcode
import short_url
from PIL import Image
from django.http import HttpResponse
from django.shortcuts import render

from config.settings.static import MEDIA_ROOT, STATIC_URL
from service.consumer.models import Profile
from .models import QRToken
from .utiils import logo_abb, merge_image


def generate_qrcode(data, size=11):
    qr = qrcode.QRCode(version=1, box_size=size, border=1, error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(data)
    qr.make(fit=True)
    im = qr.make_image()

    return im


def q(request, uid):
    uid = short_url.decode_url(uid)
    url = {
        'type': 'invite',
        'data': {
            'uri': '/api/users/%s/invite/' % uid
        }
    }

    url = json.dumps(url)

    # url = 'http://' + request.get_host() + '/api/users/%s/invite/' % uid

    white = "./service/frontend/static/frontend/images/white.png"

    try:
        obj = Profile.objects.filter(id=uid).get()
    except Profile.DoesNotExist:
        return HttpResponse('获取头像信息失败')

    if obj.avatar.name != '':
        logo = MEDIA_ROOT + '/' + obj.avatar.name
    else:
        logo = MEDIA_ROOT + "/avatar/default.jpg"

    random_list = range(1, 6)
    type = choice(random_list)

    if type == 1:
        ground = Image.open("./service/frontend/static/frontend/images/ground1.jpg")
    elif type == 2:
        ground = Image.open("./service/frontend/static/frontend/images/ground2.jpg")
    elif type == 3:
        ground = Image.open("./service/frontend/static/frontend/images/ground3.jpg")
    elif type == 4:
        ground = Image.open("./service/frontend/static/frontend/images/ground4.jpg")
    elif type == 5:
        ground = Image.open("./service/frontend/static/frontend/images/ground5.jpg")
    else:
        ground = Image.open("./service/frontend/static/frontend/images/ground1.jpg")

    img = generate_qrcode(url)

    # if img.mode != 'RGBA':
    #     img = img.convert('RGBA')

    ground_w, ground_h = ground.size

    if type == 2:
        scale = 60
    elif type == 3:
        scale = 68
    elif type == 4 or type == 5:
        scale = 64
    else:
        scale = 60

    img_w = int(ground_w / 100 * scale)
    img_h = int(ground_h / 100 * scale)

    img = logo_abb(img, img_w, img_h)  # 图片缩略
    img_w, img_h = img.size

    if type == 4 or type == 5:
        w = int((ground_w - img_w) / 2 + 2)
        h = int((ground_h - img_h) / 2 - 8)
    else:
        w = int((ground_w - img_w) / 2 + 3)
        h = int((ground_h - img_h) / 2 + 3)

    # 合并二维码与背景图
    img = merge_image(ground, img, w, h)

    if type == 1 or type == 3:
        img = logo_abb(img, 258, 258)
        temp = tempfile.mkstemp('.png')
        temp = temp[1]

        img.save(temp)
        stream = open(temp)

        return HttpResponse(stream, content_type="image/jpeg")

    image_w, image_h = img.size

    white = Image.open(white)

    white_w = int(image_w / 8)
    white_h = int(image_h / 8)

    white = logo_abb(white, white_w, white_h)  # 图片缩略

    white_w, white_h = white.size

    w = int((image_w - white_w) / 2)
    h = int((image_h - white_h) / 2)

    # 合并二维码与白色图片
    qr = merge_image(img, white, w, h)

    # logo
    logo = Image.open(logo)

    logo_w = int(image_w / 8 - 8)
    logo_h = int(image_h / 8 - 8)

    logo = logo_abb(logo, logo_w, logo_h)  # logo 缩略

    w = int((image_w - white_w) / 2 + 4)
    h = int((image_h - white_h) / 2 + 4)

    # 合并二维码与logo头像
    img = merge_image(qr, logo, w, h)

    img = logo_abb(img, 258, 258)

    temp = tempfile.mkstemp('.png')
    temp = temp[1]

    img.save(temp)
    stream = open(temp)

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
