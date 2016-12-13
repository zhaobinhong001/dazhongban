# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from rest_framework import serializers

from service.kernel.contrib.utils.hashlib import md5
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


class CallbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Validate
        fields = ('key', 'nu', 'dn')


class ValidateSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs['key'] == md5('%s%s%s' % (attrs['nu'], attrs['dn'], settings.IDDENTITY_APPKEY)).hexdigest():
            return True

        raise serializers.ValidationError('key error.')

    class Meta:
        model = Validate
        fields = ('key', 'nu', 'dn')
