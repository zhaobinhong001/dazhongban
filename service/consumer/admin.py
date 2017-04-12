# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth import get_user_model


class ConsumerAdmin(admin.ModelAdmin):
    list_display = ('username', 'date_joined', 'is_superuser', 'is_active')
    list_filter = ('is_superuser', 'is_active')
    search_fields = ('username', 'mobile')


admin.site.register(get_user_model(), ConsumerAdmin)
