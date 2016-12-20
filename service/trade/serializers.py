# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from .models import Contract, Transfer


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        exclude = ('sender', 'receiver')


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        exclude = ('sender',)
