# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from bank.models import Banklog


class BankAdmin(admin.ModelAdmin):
    '''
    银行流水
    '''
    list_display = ('title', 'amount', 'orderid', 'receive')
    # list_filter = ('creation_time', 'approval_status')
    # ordering = ('-creation_time',)
    # search_fields = ('applicant',)


admin.site.register(Banklog, BankAdmin)
