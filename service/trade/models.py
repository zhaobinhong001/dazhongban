# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

CONSUMPTION_TYPE = (
    ('0', '扫码支付'),
    ('1', '第三方支付'),
)


# 合约表
class Contract(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True,default='')
    date = models.DateTimeField(verbose_name=u'消费时间', max_length=11, auto_now_add=True)
    bank_name = models.CharField(verbose_name=u'银行名称', max_length=100)
    transaction_amount = models.DecimalField(verbose_name=u'交易金额', max_digits=10, decimal_places=2)
    turnOut_AccountNumber = models.IntegerField(verbose_name=u'转出账号')
    into_AccountNumber = models.IntegerField(verbose_name=u'转入账号')
    into_name = models.CharField(verbose_name=u'转入户名', max_length=30)
    consumption_business = models.CharField(verbose_name=u'消费商家', null=True, max_length=100)
    consumption_commodity = models.CharField(verbose_name=u'消费商品', null=True, max_length=100)
    consumption_type = models.CharField(verbose_name=u'消费类型', max_length=100, default=0, choices=CONSUMPTION_TYPE)

    def __unicode__(self):
        return '%s %s %s' % (self.bank_name, self.into_name, self.consumption_business)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = _(u'合约记录')
        verbose_name_plural = _(u'合约记录')


# 消费表
class Consumption(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True,default='')
    date = models.DateTimeField(verbose_name=u'消费时间', max_length=11, auto_now_add=True)
    bank_name = models.CharField(verbose_name=u'银行名称', max_length=100)
    transaction_amount = models.DecimalField(verbose_name=u'交易金额', max_digits=10, decimal_places=2)
    turnOut_AccountNumber = models.IntegerField(verbose_name=u'转出账号')
    into_AccountNumber = models.IntegerField(verbose_name=u'转入账号')
    into_name = models.CharField(verbose_name=u'转入户名', max_length=30)
    consumption_business = models.CharField(verbose_name=u'消费商家', null=True, max_length=100)
    consumption_commodity = models.CharField(verbose_name=u'消费商品', null=True, max_length=100)
    consumption_type = models.CharField(verbose_name=u'消费类型', max_length=100, default=0, choices=CONSUMPTION_TYPE)

    def __unicode__(self):
        return '%s %s %s' % (self.bank_name, self.into_name, self.consumption_business)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = _(u'消费记录')
        verbose_name_plural = _(u'消费记录')
