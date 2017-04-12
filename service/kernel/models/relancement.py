# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

APPROVAL_CHOICES = (
    ('1', '待审核'),
    ('2', '已发布'),
    ('3', '已驳回'),
)

OPERATION_CHOICES = (
    ('1', '全部操作系统类型'),
    ('2', 'IOS系统'),
    ('3', 'Android系统'),
)

GENDER_CHOICES = (
    ('1', '全部性别'),
    ('2', '男性用户'),
    ('3', '女性用户')
)

AGE_CHOICES = (
    ('1', '全部年龄层'),
    ('2', '20~40岁用户'),
    ('3', '40~60岁用户'),
    ('4', '60岁以上用户')
)

AUTHENTICATION_CHOICES = (
    ('1', '全部认证方式'),
    ('2', 'A 类认证'),
    ('3', 'B 类认证'),
    ('4', 'C 类认证'),
    ('5', 'D 类认证')
)

CERTIFICATES_CHOICES = (
    ('1', '全部认证类型'),
    ('2', '身份证'),
    ('3', '护照'),
    ('4', '军官证'),
    ('5', '台胞证')
)


class Relancement(models.Model):
    '''
    公告管理
    '''
    UNITS_CHOICES = ()
    title = models.CharField(verbose_name=_(u'公告标题'), max_length=50, default='')
    content = models.CharField(verbose_name=_(u'公告内容'), max_length=200, default='')
    price = models.ImageField(verbose_name=_(u'图片'), upload_to="goods", height_field='url_height',
        width_field='url_width', help_text=u'图片尺寸最好为75x75', blank=True, null=True, )
    applicant = models.CharField(verbose_name=_(u'申请人'), max_length=50, default='')
    creation_time = models.DateField(verbose_name=_(u'申请时间'), auto_now_add=True)
    # approval = models.CharField(verbose_name=_(u'审批人'), max_length=50, default='')
    operation = models.CharField(verbose_name=_(u'用户操作系统限制'), max_length=10, choices=OPERATION_CHOICES)
    gender = models.CharField(verbose_name=_(u'用户性别限制'), max_length=10, choices=GENDER_CHOICES)
    age = models.CharField(verbose_name=_(u'用户年龄限制'), max_length=10, choices=AGE_CHOICES)
    authentication = models.CharField(verbose_name=_(u'用户认证类型'), max_length=10, choices=AUTHENTICATION_CHOICES)
    certificates = models.CharField(verbose_name=_(u'用户证件类型'), max_length=10, choices=CERTIFICATES_CHOICES)
    approval_status = models.CharField(verbose_name=_(u'公告状态'), max_length=10, choices=APPROVAL_CHOICES, default='1')
    applicant_time = models.DateTimeField(verbose_name=_(u'审批时间'), auto_now=True)
    # order = models.IntegerField(_(u'排序'), default='1')

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = _(u'创建公告')
        verbose_name_plural = _(u'发布公告')
