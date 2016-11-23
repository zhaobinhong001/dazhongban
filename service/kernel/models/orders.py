# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFill

from . import Client
from . import Goods


class Orders(models.Model):
    UNITS_CHOICES = ()
    number = models.CharField(verbose_name=_(u'订单号'), max_length=100, default='', blank=False, null=False)
    address = models.DecimalField(verbose_name=_(u'价格'), max_digits=10, decimal_places=2, blank=True, null=True)
    units = models.CharField(verbose_name=_(u'单位'), max_length=50, choices=UNITS_CHOICES)
    order = models.IntegerField(_(u'排序'), default='1')

    goods = models.ForeignKey(Goods)
    client = models.ForeignKey(Client)

    def __unicode__(self):
        return '%s (%d)' % (self.name, self.total)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = _(u'订单列表')
        verbose_name_plural = _(u'订单列表')
