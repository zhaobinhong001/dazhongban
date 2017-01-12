# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from ..models.report import Report, Invite


class InviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = ('defendant', 'revelator', 'content')


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('content',)
