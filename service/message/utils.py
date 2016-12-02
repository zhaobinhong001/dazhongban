# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from rongcloud import RongCloud

appkey = settings.RONGCLOUD_APPKEY
secret = settings.RONGCLOUD_SECRET
client = RongCloud(appkey, secret)


def get_im_token(userid, name, avatar):
    ret = client.User.getToken(userId=userid, name=name, portraitUri=avatar)
    return ret.result.get('token')
