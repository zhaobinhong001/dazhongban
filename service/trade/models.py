# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

CONSUMPTION_TYPE = (
    ('0', '扫码支付'),
    ('1', '第三方支付'),
)

CONTRACT_TYPE = (
    ('receipt', '收据'),
    ('borrow', '借条'),
    ('owe', '欠条'),
)


# 合约表
class Contract(TimeStampedModel):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, default='', related_name='contract_sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, default='', related_name='contract_receiver')

    type = models.CharField(verbose_name=u'消费类型', max_length=100, default=0, choices=CONTRACT_TYPE)
    amount = models.DecimalField(verbose_name=u'交易金额', max_digits=10, decimal_places=2)
    summary = models.CharField(verbose_name=u'原因', max_length=300)
    make_date = models.DateTimeField(verbose_name=u'操作时间', blank=True, null=True)

    def __unicode__(self):
        return '%s %s %s' % (self.sender, self.receiver, self.type)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = _(u'合约记录')
        verbose_name_plural = _(u'合约记录')


# 消费表
class Transfer(TimeStampedModel):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, default='', related_name='transfer_sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, default='', related_name='transfer_receiver')

    type = models.CharField(verbose_name=u'消费类型', max_length=100, default=0, choices=CONTRACT_TYPE)
    amount = models.DecimalField(verbose_name=u'交易金额', max_digits=10, decimal_places=2)
    summary = models.CharField(verbose_name=u'原因', max_length=300)
    transfer = models.CharField(verbose_name=u'转出银行卡', max_length=100, default='')

    def __unicode__(self):
        return '%s %s %s' % (self.sender, self.receiver, self.type)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = _(u'消费记录')
        verbose_name_plural = _(u'消费记录')
