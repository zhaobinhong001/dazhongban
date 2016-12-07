# -*- coding: utf-8 -*-
# dashboard/views.py

from __future__ import unicode_literals

from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from requests import request
from rest_framework.permissions import IsAuthenticated
from suit_dashboard.views import DashboardView
from service.consumer.models import Profile

# from .boxes import User, Authentication, SettledEnterprise, Evidences, Signatures, BasicLine
from service.consumer.serializers import SettingsSerializer
from service.consumer.utils import get_user_settings


# class HomeView(DashboardView):
#
#     # str = ("title = %s, category = %s, date_time = %s, content = %s"
#     #        % (post.title, post.category, post.date_time, post.content))
#     template_name = "abc.html"

def abc(request):
        post = Profile.objects.all()
        return render(request, 'abc.html', {'post': post})


#     grid = Grid(Row(Column(User(), width=4), Column(Authentication(), width=4), Column(SettledEnterprise(), width=4),
#                     Column(Signatures(), width=4), Column(Evidences(), width=4)))
#
#
# class LineView(DashboardView):
#     template_name = 'data.html'
#     crumbs = (
#         {'url': 'admin:data', 'name': _('数据')},
#     )
#     grid = Grid(Row(Column(BasicLine(), width=12)))
#
#
# def link(request):
#     return render(request, 'data.html')
