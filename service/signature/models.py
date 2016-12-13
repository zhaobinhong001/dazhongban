# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel


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


BANKID = (
    ('542', u'重庆三峡银行'),
    ('100', u'邮政储蓄银行'),
    ('102', u'中国工商银行'),
    ('103', u'中国农业银行'),
    ('104', u'中国银行'),
    ('105', u'中国建设银行'),
    ('301', u'交通银行'),
    ('302', u'中信银行'),
    ('303', u'中国光大银行'),
    ('304', u'华夏银行'),
    ('305', u'中国民生银行'),
    ('306', u'广东发展银行'),
    ('307', u'平安银行'),
    ('308', u'招商银行'),
    ('309', u'兴业银行'),
    ('310', u'上海浦东发展银行'),
    ('311', u'恒丰银行'),
    ('316', u'浙商银行'),
    ('317', u'渤海银行'),
    ('422', u'河北银行'),
    ('401', u'上海银行'),
    ('403', u'北京银行'),
    ('424', u'南京银行'),
    ('423', u'杭州银行'),
    ('434', u'天津银行'),
    ('408', u'宁波银行'),
    ('409', u'齐鲁银行'),
    ('440', u'徽商银行'),
    ('442', u'哈尔滨银行'),
    ('443', u'贵阳银行'),
    ('447', u'兰州银行'),
    ('448', u'南昌银行'),
    ('450', u'青岛银行'),
    ('888', u'中金网银无卡'),
    ('889', u'中金网银'),
    ('891', u'金科无卡'),
    ('892', u'银联代扣'),
    ('900', u'收单机构（900）'),
    ('700', u'CFCA模拟银行'),
    ('1405', u'广东农商行'),
    ('1565', u'颖淮农商行'),
    ('1513', u'重庆农村商业银行'),

)


class Identity(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    certId = models.CharField(verbose_name=u'证件号', max_length=100, default='')
    certType = models.IntegerField(verbose_name=u'证件类型', default='1')
    name = models.CharField(verbose_name=u'姓名', max_length=50, default='')
    phone = models.CharField(verbose_name=u'电话', max_length=100, default='')
    originType = models.IntegerField(verbose_name=u'渠道类型 ', default='1')
    address = models.CharField(verbose_name=u'地址', max_length=200, default='', null=True, blank=True)
    frontPhoto = models.ImageField(verbose_name=u'证件照正面')
    backPhoto = models.ImageField(verbose_name=u'证件照反面')
    cardNo = models.CharField(verbose_name=u'银行卡号', max_length=100, default='')
    bankID = models.CharField(verbose_name=u'银行ID', max_length=100, default='', choices=BANKID)
    cvn2 = models.CharField(verbose_name=u'信用卡背面的末3位数字', max_length=10, default='', null=True, blank=True)
    expired = models.DateField(verbose_name=u'有效期', max_length=100, default='', null=True, blank=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = u'身份认证'
        verbose_name_plural = u'身份认证'
