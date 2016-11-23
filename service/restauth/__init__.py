# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

default_app_config = 'service.restauth.RestauthConfig'


class RestauthConfig(AppConfig):
    name = 'service.restauth'
    verbose_name = _(u'Restful 认证')
