# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from .models import Signature, Validate, Identity


class IdentitySerializer(serializers.ModelSerializer):
    # idcard = serializers.CharField(label=u'身份证号码')
    # name = serializers.CharField(label=u'客户姓名')
    # phone = serializers.CharField(label=u'预留电话')
    # originType = serializers.IntegerField(label=u'渠道类型', default=1)
    # bankcard = serializers.CharField(label=u'银行卡号')
    # frontPhoto = serializers.FileField(label=u'身份证证明')
    # backPhoto = serializers.FileField(label=u'身份证反面')

    class Meta:
        model = Identity
        # exclude = ('owner',)
        fields = '__all__'


class SignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signature
        exclude = ('owner',)


class ValidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Validate
        fields = ('key', 'dn')
