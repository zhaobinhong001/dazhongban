# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random

from django.conf import settings
from model_utils.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _

from django.db import models

from config.settings.auth import AUTH_USER_MODEL


class WaterLog(TimeStampedModel):
    '''
    流水日志
    '''
    appkey = models.CharField(verbose_name=_(u'唯一标示'), max_length=100, default='')
    openid = models.CharField(verbose_name=_(u'用户对应的唯一码'), max_length=100, default='')
    owner = models.ForeignKey(AUTH_USER_MODEL)

    def save(self, *args, **kwargs):
        self.openid = str(random.randint(0, 999999)).zfill(6)
        super(self.__class__, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _(u'日志')
        verbose_name_plural = _(u'日志')
