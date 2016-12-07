# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cStringIO import StringIO

import qrcode
import short_url
from django.http import HttpResponse


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
