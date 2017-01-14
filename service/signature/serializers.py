# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
from django.conf import settings
from rest_framework import serializers

from service.kernel.contrib.utils.hashlib import md5
from .models import Signature, Validate, Identity


class BankcardSerializer(serializers.Serializer):
    card = serializers.CharField(label=u'银行卡号')
    name = serializers.CharField(label=u'卡片名称', default='', read_only=True)
    bank = serializers.CharField(label=u'银行名称', default='', read_only=True)
    type = serializers.CharField(label=u'卡片类型', default='', read_only=True)
    bankID = serializers.CharField(label=u'银行编号', default='', read_only=True)

    def validate(self, attrs):
        # 验证银行卡号
        resp = requests.post(url=settings.BANK_CARD, data=attrs)
        data = resp.json()

        if data['status'] == -1:
            raise serializers.ValidationError('银行卡不能为空.')
        elif data['status'] == -2:
            raise serializers.ValidationError('输入的银行卡位数不正确.')
        elif data['status'] == 0:
            raise serializers.ValidationError('未找到该类型卡信息,请确认卡号书写正确.')
        else:
            return data['result']


class IdentitySerializer(serializers.ModelSerializer):
    credit = serializers.StringRelatedField(source='owner.credit')

    class Meta:
        model = Identity
        exclude = ('owner',)
        read_only_fields = ('serial', 'enddate')


class SignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signature
        fields = ('id', 'created', 'type', 'extra')


class CertificateSerializer(serializers.Serializer):
    dn = serializers.CharField()
    reissue = serializers.BooleanField(label=u'自动补发')

    class Meta:
        fields = ('dn',)


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
