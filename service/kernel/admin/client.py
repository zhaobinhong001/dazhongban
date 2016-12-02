# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from reversion.admin import VersionAdmin

from ..models import Address
from ..models import Client


class AddressAdmin(VersionAdmin):
    pass


class ClientAdmin(VersionAdmin):
    pass


# admin.site.register(Address, AddressAdmin)
# admin.site.register(Client, ClientAdmin)
