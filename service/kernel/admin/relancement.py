# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from ..models.relancement import Relancement


class RelancementAdmin(admin.ModelAdmin):
    '''
    公告管理
    '''
    list_display = ('applicant', 'content', 'approval_status', 'creation_time')
    list_filter = ('creation_time', 'approval_status')
    ordering = ('-creation_time',)
    search_fields = ('applicant',)

admin.site.register(Relancement, RelancementAdmin)
