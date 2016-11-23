# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from imagekit.models import ProcessedImageField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from pilkit.processors import ResizeToFill


class Groups(MPTTModel):
    name = models.CharField(verbose_name=_(u'分类名称'), max_length=64, null=False)
    slug = models.SlugField(verbose_name=_(u'Slug'), default='', blank=True, null=True)
    cover = models.ImageField(verbose_name=_(u'分类图片'), max_length=200, blank=True, upload_to='category')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    ordering = models.PositiveIntegerField(verbose_name=_(u'排序'), default=999, editable=False)
    is_active = models.BooleanField(verbose_name=_(u'激活'), default=False)
    keyword = models.CharField(verbose_name=_(u'分类关键字'), max_length=100, null=True, blank=True)
    channel = models.CharField(verbose_name=_(u'频道'), max_length=100, null=True, blank=True)
    catids = models.BigIntegerField(verbose_name=_(u'淘宝分类'), blank=True, null=True)
    total = models.IntegerField(verbose_name=_(u'商品数'), blank=True, null=True, default=0)

    def __unicode__(self):
        return '%s (%d)' % (self.name, self.total)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = _(u'客户分组')
        verbose_name_plural = _(u'客户分组')

    class MPTTMeta:
        order_insertion_by = ['ordering']
        parent_attr = 'parent'


class Client(models.Model):
    UNITS_CHOICES = ()
    name = models.CharField(verbose_name=_(u'名称'), max_length=100, default='')
    price = models.DecimalField(verbose_name=_(u'价格'), max_digits=10, decimal_places=2, blank=True, null=True)
    units = models.CharField(verbose_name=_(u'单位'), max_length=50, choices=UNITS_CHOICES)
    order = models.IntegerField(_(u'排序'), default='1')
    cover = ProcessedImageField(verbose_name=_(u'图片'), upload_to='goods', processors=[ResizeToFill(720, 240)],
        format='JPEG', null=True, help_text=u'图片尺寸最好为720x240')

    groups = models.ForeignKey(Groups)

    def __unicode__(self):
        return '%s (%d)' % (self.name, self.total)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = _(u'客户列表')
        verbose_name_plural = _(u'客户列表')


class Address(models.Model):
    area = models.CharField(_(u'地区'), max_length=50, default='')
    site = models.CharField(_(u'城市'), max_length=50, default='')
    address = models.CharField(_(u'详细地址'), max_length=200, blank=True, null=True)

    client = models.ForeignKey(Client)

    def __unicode__(self):
        return '%s %s' % (self.site, self.address)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = _(u'客户地址')
        verbose_name_plural = _(u'客户地址')
