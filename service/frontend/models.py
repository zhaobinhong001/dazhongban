# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib
import random

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel, StatusModel


class QRToken(TimeStampedModel, StatusModel):
    '''
    扫码登陆

    '''
    STATUS = Choices('init', 'scan', 'done', 'cancel')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, default='', blank=True, null=True)
    key = models.CharField(verbose_name=u'扫码唯一标识', blank=True, max_length=50, default='')
    raw = models.TextField(verbose_name=u'原始数据')

    def generate_code(self):
        randomNum = str(random.randint(0, 999999)).zfill(6)
        md1 = hashlib.md5()
        md1.update(randomNum)
        key = md1.hexdigest()
        return key

    def save(self, *args, **kwargs):
        self.key = self.generate_code()
        super(self.__class__, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.key

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = _(u'扫码登陆')
        verbose_name_plural = _(u'扫码登陆')
