# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from reversion.admin import VersionAdmin

from ..models.consumption import Consumption


class ConsumptionAdmin(VersionAdmin):
    pass


admin.site.register(Consumption, ConsumptionAdmin)
