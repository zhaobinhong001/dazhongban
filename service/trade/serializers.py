# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from .models import Consumption, Contract


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'


class ConsumptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumption
        fields = '__all__'
