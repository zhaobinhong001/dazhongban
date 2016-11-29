# -*- coding: utf-8 -*-
# dashboard/views.py

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from suit_dashboard.layout import Grid, Row, Column
from suit_dashboard.views import DashboardView

from .boxes import BoxMachine


class HomeView(DashboardView):
    template_name = 'main.html'
    crumbs = (
        {'url': 'admin:index', 'name': _('Home')},
    )
    grid = Grid(Row(Column(BoxMachine(), width=6)))
