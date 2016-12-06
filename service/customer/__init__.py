# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

default_app_config = 'service.customer.CustomerConfig'


class CustomerConfig(AppConfig):
    name = 'service.customer'
    verbose_name = _(u'django模板')
