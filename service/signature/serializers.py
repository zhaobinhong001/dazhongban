# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from .models import Signature, Validate, Identity


class BankcardSerializer(serializers.Serializer):
    card = serializers.CharField(label=u'银行卡号')
    name = serializers.CharField(label=u'银行名称')


class IdentitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Identity
        exclude = ('owner', 'certType', 'originType')


class SignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signature
        exclude = ('owner',)


class ValidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Validate
        fields = ('key', 'dn')
