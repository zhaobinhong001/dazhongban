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


class Validate(TimeStampedModel):
    key = models.CharField(max_length=200, default='', unique=True)
    dn = models.CharField(max_length=200, default='')

    def __unicode__(self):
        return self.signs

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = u'身份验证'
        verbose_name_plural = u'身份验证'


class Identity(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(verbose_name=u'姓名', max_length=50, default='')
    phone = models.CharField(verbose_name=u'电话', max_length=100, default='')
    certId = models.CharField(verbose_name=u'身份证', max_length=100, default='')
    cardNo = models.CharField(verbose_name=u'银行卡号', max_length=100, default='')
    bankID = models.CharField(verbose_name=u'银行卡号', max_length=100, default='')
    expired = models.CharField(verbose_name=u'过期时间', max_length=100, default='')
    certType = models.IntegerField(verbose_name=u'卡片类型', default='1')
    address = models.CharField(verbose_name=u'详细地址', max_length=200, default='')
    frontPhoto = models.CharField(verbose_name=u'详细地址', max_length=200, default='')
    backPhoto = models.CharField(verbose_name=u'详细地址', max_length=200, default='')
    cvn2 = models.CharField(verbose_name=u'详细地址', max_length=200, default='')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = u'身份认证'
        verbose_name_plural = u'身份认证'
