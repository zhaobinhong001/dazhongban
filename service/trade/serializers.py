# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from service.trade.models import Purchased
from .models import Contract, Transfer


class ContractSerializer(serializers.ModelSerializer):
    # sender_nick = serializers.StringRelatedField(read_only=True, source='sender.profile.nick')
    # sender_name = serializers.StringRelatedField(read_only=True, source='sender.profile.name')

    # receiver_nick = serializers.StringRelatedField(read_only=True, source='receiver.profile.nick')
    # receiver_name = serializers.StringRelatedField(read_only=True, source='receiver.profile.name')

    class Meta:
        model = Contract
        exclude = ('sender', 'receiver')


class ContractDetailSerializer(serializers.ModelSerializer):
    sender_nick = serializers.StringRelatedField(read_only=True, source='sender.profile.nick')
    sender_name = serializers.StringRelatedField(read_only=True, source='sender.profile.name')

    receiver_nick = serializers.StringRelatedField(read_only=True, source='receiver.profile.nick')
    receiver_name = serializers.StringRelatedField(read_only=True, source='receiver.profile.name')
    description = serializers.CharField()

    receiver_serial = serializers.StringRelatedField(read_only=True, source='receiver_sign.serial')
    sender_serial = serializers.StringRelatedField(read_only=True, source='sender_sign.serial')

    class Meta:
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
