# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

CHATBOT_DEFUALT = {
    'SESSION_PATH': 'runtime/itchat.kpl',
    'QR_CODE_PATH': 'runtime/itchat.png',
    'DEBUG': settings.DEBUG,
}
