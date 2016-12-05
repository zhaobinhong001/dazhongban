# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel


class Signature(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='signatures')
    signs = models.TextField(verbose_name=u'证书密文', default='')
    created_at = models.DateField(auto_now=True)

    def __unicode__(self):
        return self.signs

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = u'签名证书'
        verbose_name_plural = u'签名证书'


class Identity(TimeStampedModel):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='identity')
    signs = models.TextField(verbose_name=u'证书密文', default='')
    name = models.CharField(verbose_name=u'姓名', max_length=50, default='')
    phone = models.CharField(verbose_name=u'电话', max_length=100, default='')
    id_card = models.CharField(verbose_name=u'身份证', max_length=100, default='')
    bankcard = models.CharField(verbose_name=u'银行卡号', max_length=100, default='')
    expired = models.CharField(verbose_name=u'过期时间', max_length=100, default='')
    card_type = models.CharField(verbose_name=u'卡片类型', max_length=100, default='')

    def __unicode__(self):
        return self.signs

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = u'身份认证'
        verbose_name_plural = u'身份认证'
