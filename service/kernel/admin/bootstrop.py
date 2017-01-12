# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from reversion.admin import VersionAdmin

from ..models.bootstrap import Version


class VersionsAdmin(VersionAdmin):
    list_display = ('version', 'platform', 'channel', 'sha1sum')


admin.site.register(Version, VersionsAdmin)
