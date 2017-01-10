# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from service.consumer.models import Bankcard


def run():
    Bankcard.objects.filter(bank=u'收付宝').delete()
