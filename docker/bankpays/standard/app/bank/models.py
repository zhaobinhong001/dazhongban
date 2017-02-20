# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Banklog(models.Model):
    '''
    公告管理
    '''
    receive = models.CharField(verbose_name=_(u'收款方名字'), max_length=64, default='')
    orderid = models.CharField(verbose_name=u'订单号码', max_length=100, default='')
    amount = models.DecimalField(verbose_name=u'交易金额', max_digits=10, decimal_places=2, default='')
    title = models.CharField(verbose_name=u'商品名称', max_length=100, default='')

    class Meta:
        verbose_name = _(u'银行流水')
        verbose_name_plural = _(u'银行流水')
