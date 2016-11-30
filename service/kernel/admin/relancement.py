# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from reversion.admin import VersionAdmin
from ..models.relancement import Relancement


class RelancementAdmin(admin.ModelAdmin):

    list_display = ('applicant', 'content', 'approval_status', 'creation_time')
    list_filter = ('creation_time', 'approval_status')
    ordering = ('-creation_time',)
    search_fields = ('applicant',)

    # fields = ('creation_time',)
    # form = VerifyCodeForm
    # def has_add_permission(self, request):
    #     pass
    #
    # def has_delete_permission(self, request, obj=None):
    #     pass

    # <span style ="color: #ff0000;"> search_fields = ('title', 'pro_address')</span>
admin.site.register(Relancement, RelancementAdmin)

