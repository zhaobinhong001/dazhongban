# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from service.frontend.models import QRToken
from service.signature import serializers


class ScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRToken
        fields = '__all__'
