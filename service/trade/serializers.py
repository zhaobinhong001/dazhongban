# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from rest_framework import serializers

from service.trade.models import Purchased
from .models import Contract, Transfer


class SenderSerializer(serializers.ModelSerializer):
    nick = serializers.StringRelatedField(read_only=True, source='profile.nick')
    originType = serializers.StringRelatedField(source='identity.originType')
    certType = serializers.StringRelatedField(source='identity.certType')
    enddate = serializers.StringRelatedField(source='identity.enddate')
    certId = serializers.StringRelatedField(source='identity.certId')
    serial = serializers.StringRelatedField(source='identity.serial')
    name = serializers.StringRelatedField(source='identity.name')

    class Meta:
        model = get_user_model()
        fields = (
        'id', 'name', 'nick', 'level', 'credit', 'certId', 'enddate', 'serial', 'originType', 'certType', 'identity')


class ReceiverSerializer(SenderSerializer):
    pass


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        exclude = ('sender', 'receiver')


class ContractDetailSerializer(serializers.ModelSerializer):
    description = serializers.CharField()
    receiver = ReceiverSerializer()
    sender = SenderSerializer()

    class Meta:
        depth = 1
        model = Contract
        fields = '__all__'


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        exclude = ('sender',)


class PurchasedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchased
        exclude = ('owner',)
