# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from reversion.admin import VersionAdmin
from service.kernel.models.bootstrap import Version


class VerAdmin(VersionAdmin):
    pass


admin.site.register(Version, VerAdmin)
