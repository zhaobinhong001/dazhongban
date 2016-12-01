# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from ..models.relancement import Relancement


class RelancementAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'content', 'approval_status', 'creation_time')
    list_filter = ('applicant', 'creation_time', 'approval_status')


admin.site.register(Relancement, RelancementAdmin)
