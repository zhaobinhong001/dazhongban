# coding:utf-8
from __future__ import unicode_literals

from django.db import models

CREDENTIALS_TYPE = (
    ('0', '身份证'),
    ('1', 'EID'),
    ('2', '3')
)

CREDENTIALS_LEVEL = (
    ('0', 'A'),
    ('1', 'B'),
    ('2', 'C'),
    ('3', 'D'),
)

CREDIT_LEVEL = (
    ('0', 'A-10'),
    ('1', 'B-10'),
    ('2', 'C-10'),
)
AURGENTICATION_MODE = (
    ('0', '远程柜台'),
    ('1', '银行柜台'),
)


# 数字证书表
class Certufucate(models.Model):
    certufucate_num = models.IntegerField(verbose_name=u'证书号')
    certufucate_name = models.CharField(verbose_name=u'证书持有人', max_length=100)
    credentials_type = models.IntegerField(verbose_name=u'证件类型', choices=CREDENTIALS_TYPE, default=0)  # 证件类型一共几种
    credentials_num = models.CharField(verbose_name=u'证件号', max_length=100)
    certification_authority = models.CharField(verbose_name=u'发证机构', max_length=100)
    certufucate_status = models.BooleanField(verbose_name=u'证书状态', default=True)  # True:正常；False:异常
    certufucate_level = models.CharField(verbose_name=u'证书等级', max_length=10, default=0, choices=CREDENTIALS_LEVEL)
    authentication_mode = models.CharField(verbose_name=u'认证方式', default=0, max_length=10, choices=AURGENTICATION_MODE)
    credit_level = models.CharField(verbose_name=u'信用等级', choices=CREDIT_LEVEL, max_length=100)
    termOfValidity = models.DateTimeField(verbose_name=u'有效期', max_length=11)

    # aaa=models.CharField(max_length=100,verbose_name=111,choices=CHANNEL_CHOICES,default=1001)

    def __unicode__(self):
        return '%s %s' % (self.certufucate_name, self.certification_authority)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = (u'数字证书')
        verbose_name_plural = (u'数字证书')
