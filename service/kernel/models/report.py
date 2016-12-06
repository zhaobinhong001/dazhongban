# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel, StatusModel


class Invite(TimeStampedModel, StatusModel):
    STATUS = Choices('draft', 'published')
    defendant = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True, verbose_name=_(u'被举报人'))
    revelator = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True, verbose_name=_(u'揭发者'))
    content = models.TextField(verbose_name=_(u'举报内容'))


class Report(TimeStampedModel, StatusModel):
    STATUS = Choices('draft', 'published')
    defendant = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True, verbose_name=_(u'被举报人'))
    revelator = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True, verbose_name=_(u'揭发者'))
    content = models.TextField(verbose_name=_(u'举报内容'))

    def __unicode__(self):
        return self.defendant

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = _(u'用户举报')
        verbose_name_plural = _(u'用户举报')
