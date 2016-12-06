# -*- coding: utf-8 -*-
# dashboard/sites.py

from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib.admin.sites import AdminSite

from .views import HomeView, LineView


class DashboardSite(AdminSite):
    """A Django AdminSite to allow registering custom dashboard views."""

    def get_urls(self):
        urls = super(DashboardSite, self).get_urls()
        custom_urls = [
            url(r'^$', self.admin_view(HomeView.as_view()), name='index'),
            url(r'^data/$', self.admin_view(LineView.as_view()), name='data'),
        ]

        del urls[0]
        return custom_urls + urls
