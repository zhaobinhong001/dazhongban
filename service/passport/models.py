# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import random
import time

from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

from django.conf import settings


class WaterLog(TimeStampedModel):
    '''
    流水日志
    '''
    appkey = models.CharField(verbose_name=_(u'唯一标示'), max_length=100, default='')
    openid = models.CharField(verbose_name=_(u'用户对应的唯一码'), max_length=100, default='')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    def save(self, *args, **kwargs):
        nowTime = int(time.mktime(datetime.datetime.now().timetuple()))  # 生成当前时间
        randomNum = str(random.randint(0, 999999)).zfill(3)
        self.openid = randomNum + str(nowTime)
        super(self.__class__, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _(u'日志')
        verbose_name_plural = _(u'日志')
