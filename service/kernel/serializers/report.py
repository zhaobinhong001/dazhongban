# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from ..models.report import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('defendant', 'revelator', 'content')
        # defendant
        # revelator
