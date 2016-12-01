# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from ..contrib.utils.imports import import_submodules


class ReadonlyModelAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        opts = self.opts
        view_permission = 'view_%s' % self.model._meta.module_name
        return request.user.has_perm(opts.app_label + '.' + view_permission)

    def has_change_permission(self, request, obj=None):
        if hasattr(self, 'has_change'):
            if self.has_change:
                return True

        return super(ReadonlyModelAdmin, self).has_change_permission(request, obj)

    def get_model_perms(self, request):
        value = super(ReadonlyModelAdmin, self).get_model_perms(request)
        value['view'] = self.has_view_permission(request)

        return value

    def changelist_view(self, request, extra_context=None):
        if self.has_view_permission(request, None):
            self.has_change = True

        result = super(ReadonlyModelAdmin, self).changelist_view(request, extra_context)
        self.has_change = False
        return result


import_submodules(locals(), __name__, __path__)
