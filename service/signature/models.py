# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel


class Signature(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='signatures')
    signs = models.TextField(verbose_name=u'证书密文', default='')

    def __unicode__(self):
        return self.created

    class Meta:
        verbose_name = u'签名证书'
        verbose_name_plural = u'签名证书'
