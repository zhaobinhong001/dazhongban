# -*- coding: utf-8 -*-
# dashboard/views.py

from __future__ import unicode_literals

from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from suit_dashboard.layout import Grid, Row, Column
from suit_dashboard.views import DashboardView

from .boxes import User, Authentication, SettledEnterprise, Evidences, Signatures, BasicLine


class HomeView(DashboardView):
    template_name = "main.html"
    crumbs = (
        {'url': 'admin:index', 'name': _('Home')},
    )
    grid = Grid(Row(Column(User(), width=4), Column(Authentication(), width=4), Column(SettledEnterprise(), width=4),
        Column(Signatures(), width=4), Column(Evidences(), width=4)))


class LineView(DashboardView):
    template_name = 'data.html'
    crumbs = (
        {'url': 'admin:data', 'name': _('数据')},
    )
    grid = Grid(Row(Column(BasicLine(), width=12)))


def link(request):
    return render(request, 'data.html')
