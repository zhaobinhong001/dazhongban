# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pandas as pd
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
        df = pd.read_hdf('./resources/bankcard.h5')

        for x in [8, 6, 5]:
            vv = df.loc[df['card'] == attrs['card'][:x]]
            if len(vv):
                vv = vv.iloc[0]
                del vv['card']
                del vv['oldcard']
                attrs.update(vv)
                return attrs

        raise serializers.ValidationError('未找到该类型卡信息,请确认卡号书写正确.')


class IdentitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Identity
        exclude = ('owner', 'certType', 'originType',)
        # read_only_fields = ('dn',)


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
