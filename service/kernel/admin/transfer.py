# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from reversion.admin import VersionAdmin
from ..models.transfer import Transfer


class TransferAdmin(VersionAdmin):
    pass


admin.site.register(Transfer, TransferAdmin)
