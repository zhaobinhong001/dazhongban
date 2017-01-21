# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import jsonfield
from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel

from config.settings.apps import BANKID
from service.trade.models import CONTRACT_TYPE


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
    type = models.CharField(verbose_name=u'签名类型', max_length=100, choices=CONTRACT_TYPE)
    extra = jsonfield.JSONField(verbose_name=u'附加内容', default={'data': None, 'type': None})
    signs = models.TextField(verbose_name=u'证书密文', default='')
    serial = models.CharField(verbose_name=u'证书号', max_length=200, default='')
    expired = models.DateField(verbose_name=u'过期时间', blank=True, null=True)

    # content_object = GenericForeignKey('content_type', 'object_id')
    # content_type = models.ForeignKey(ContentType)
    # object_id = models.PositiveIntegerField()

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
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='identity')
    certId = models.CharField(verbose_name=u'证件号 *', max_length=100, default='')
    certType = models.IntegerField(verbose_name=u'证件类型', default='1', help_text=u'冗余项,不需要输入')
    name = models.CharField(verbose_name=u'姓名 *', max_length=50, default='')
    phone = models.CharField(verbose_name=u'电话 *', max_length=100, default='')
    originType = models.IntegerField(verbose_name=u'渠道类型 ', default='1', help_text=u'冗余项,不需要输入')
    address = models.CharField(verbose_name=u'地址', max_length=200, default='', null=True, blank=True)
    frontPhoto = models.ImageField(verbose_name=u'证件照正面 *', upload_to='identity')
    backPhoto = models.ImageField(verbose_name=u'证件照反面 *', upload_to='identity')
    cardNo = models.CharField(verbose_name=u'银行卡号', max_length=100, default='')
    bankID = models.CharField(verbose_name=u'银行ID', max_length=100, default='', choices=BANKID)
    cvn2 = models.CharField(verbose_name=u'信用卡背面的末3位数字', max_length=10, default='', null=True, blank=True,
        help_text=u'如果是信用卡则必须填写')
    dn = models.CharField(verbose_name=u'DN', max_length=200, default='', null=True, blank=True)
    expired = models.CharField(verbose_name=u'有效期', max_length=100, default='', null=True, blank=True,
        help_text=u'如果是信用卡则必须填写')
    level = models.CharField(verbose_name=u'认证级别 *', max_length=100, default='', null=True, blank=True,
        choices=CHOICES_LEVEL)

    serial = models.CharField(verbose_name=u'证书编号', max_length=100, null=True, blank=True, default='')
    enddate = models.CharField(verbose_name=u'证书过期时间', max_length=100, blank=True, null=True, default='')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = u'身份认证'
        verbose_name_plural = u'身份认证'


class Counter(TimeStampedModel):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='counter')
    secret = models.CharField(verbose_name=u'授权码', max_length=100, default='', null=True, blank=True)
    verify = models.CharField(verbose_name=u'验证码', max_length=100, default='', null=True, blank=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = u'临柜授权'
        verbose_name_plural = u'临柜授权'
