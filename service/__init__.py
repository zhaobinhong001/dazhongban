#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#  Copyright © XYM
# Last modified: 2016-10-18 18:26:05

# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

__version__ = '1.0.0'
default_app_config = 'service.KernelConfig'


class KernelConfig(AppConfig):
    name = 'service.kernel'
    verbose_name = _(u'赢大盘')
