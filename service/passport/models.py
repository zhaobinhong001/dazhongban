# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from model_utils.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _

from django.db import models


class WaterLog(TimeStampedModel):
    '''
    流水日志
    '''
    action = models.CharField(verbose_name=_(u'操作'), max_length=64, default='0')
    stare = models.CharField(verbose_name=_(u'状态'), max_length=10, default='0')

    def save(self, *args, **kwargs):
        super(self.__class__, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _(u'日志')
        verbose_name_plural = _(u'日志')
