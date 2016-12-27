# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import jsonfield
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db import models
from model_utils.models import TimeStampedModel

from config.settings.apps import BANKID
from service.trade.models import CONTRACT_TYPE
from django.contrib.contenttypes.models import ContentType

class Bankcard(TimeStampedModel):
    card = models.CharField(verbose_name=u'银行卡号', max_length=200, default='')
    name = models.CharField(verbose_name=u'银行名称', max_length=200, default='')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = u'银行卡片'
        verbose_name_plural = u'银行卡片'


class Signature(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='signatures')
    signs = models.TextField(verbose_name=u'证书密文', default='')
    type = models.CharField(verbose_name=u'签名类型', max_length=100, choices=CONTRACT_TYPE)
    extra = jsonfield.JSONField(verbose_name=u'附加内容', default={'data': None, 'type': None})

    content_object = GenericForeignKey('content_type', 'object_id')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()

    def __unicode__(self):
            return '%s - %s' % (self.created, self.type)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = u'签名证书'
        verbose_name_plural = u'签名证书'


class Validate(TimeStampedModel):
    key = models.CharField(max_length=200, default='', unique=True)
    nu = models.CharField(max_length=200, default='', unique=True)
    dn = models.CharField(max_length=200, default='')

    def __unicode__(self):
        return self.signs

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = u'身份验证'
        verbose_name_plural = u'身份验证'


class Identity(TimeStampedModel):
    CHOICES_LEVEL = (('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'),)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    certId = models.CharField(verbose_name=u'证件号 *', max_length=100, default='')
    certType = models.IntegerField(verbose_name=u'证件类型', default='1')
    name = models.CharField(verbose_name=u'姓名 *', max_length=50, default='')
    phone = models.CharField(verbose_name=u'电话 *', max_length=100, default='')
    originType = models.IntegerField(verbose_name=u'渠道类型 ', default='1')
    address = models.CharField(verbose_name=u'地址', max_length=200, default='', null=True, blank=True)
    frontPhoto = models.ImageField(verbose_name=u'证件照正面')
    backPhoto = models.ImageField(verbose_name=u'证件照反面')
    cardNo = models.CharField(verbose_name=u'银行卡号', max_length=100, default='')
    bankID = models.CharField(verbose_name=u'银行ID', max_length=100, default='', choices=BANKID)
    cvn2 = models.CharField(verbose_name=u'信用卡背面的末3位数字', max_length=10, default='', null=True, blank=True)
    expired = models.CharField(verbose_name=u'有效期', max_length=100, default='', null=True, blank=True)
    level = models.CharField(verbose_name=u'认证级别', max_length=100, default='', null=True, blank=True,
        choices=CHOICES_LEVEL)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

    # def save(self, *args, **kwargs):
    #     self.owner.update(level=self.level)
    #     super(self.__class__, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u'身份认证'
        verbose_name_plural = u'身份认证'
