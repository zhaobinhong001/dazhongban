# coding:utf-8
from __future__ import unicode_literals

from django.contrib import admin
from reversion.admin import VersionAdmin
from ..models.certufucate import Certufucate


class CertufucateAdmin(VersionAdmin):
    # 规则
    #  list_display = ('name','price')
    # list_editable = ('price',)
    pass


admin.site.register(Certufucate, CertufucateAdmin)
