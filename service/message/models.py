# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models


class Groups(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='im_groups')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='users')
    name = models.CharField(verbose_name=u'群组名称', max_length=100, blank=False)


class Token(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='im_token')
    key = models.CharField(verbose_name=u'Token', max_length=200, blank=False)
