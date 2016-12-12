# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random

from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel


class VerifyCode(TimeStampedModel):
    '''
    手机验证码
    '''
    STATUS = Choices(('ready', _('已读')), ('unread', _('未读')))
    mobile = models.CharField(verbose_name=_(u'手机号'), max_length=64, unique=True)
    code = models.CharField(verbose_name=_(u'验证码'), max_length=10, default='0')
    status = models.CharField(verbose_name=_(u'状态'), max_length=10, choices=STATUS)

    def generate_verification_code(self):
        return str(random.randint(0, 999999)).zfill(6)

    def save(self, *args, **kwargs):
        self.code = self.generate_verification_code()
        super(self.__class__, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _(u'验证码')
        verbose_name_plural = _(u'验证码')
