# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from service.frontend.models import QRToken


class ScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRToken
        fields = '__all__'