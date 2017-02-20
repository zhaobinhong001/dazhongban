# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import Address, Profile, Contact, Bankcard, Contains, Notice


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class ProfileSerializer(serializers.ModelSerializer):
    level = serializers.StringRelatedField(source='owner.level', default='')
    credit = serializers.StringRelatedField(source='owner.credit', default='')
    mobile = serializers.StringRelatedField(source='owner.mobile', default='')
    name = serializers.StringRelatedField(source='owner.identity.name', default='')
    idcard = serializers.StringRelatedField(source='owner.identity.certId', default='')
    bankcard = serializers.StringRelatedField(source='owner.identity.cardNo', default='')
    certType = serializers.StringRelatedField(source='owner.identity.certType', default='')

    birthday = serializers.DateField(default='')

    class Meta:
        model = Profile
        read_only_fields = ("name", "phone", "qr", "level", 'bankcard', 'idcard', 'credit', 'certType')
        fields = (
            "name", "nick", "phone", "mobile", "gender", "birthday", "qr", 'level', 'idcard', 'bankcard', 'avatar',
            'credit', 'certType')


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='profile.name', label=u'姓名')
    nick = serializers.CharField(source='profile.nick', label=u'昵称')
    avatar = serializers.ImageField(source='profile.avatar', label=u'头像')

    class Meta:
        model = get_user_model()
        fields = ('id', 'name', 'nick', 'avatar', 'mobile', 'level', 'avatar')


class NickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("nick",)


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("avatar",)


class AddFriendSerializer(serializers.Serializer):
    userid = serializers.IntegerField(label='用户id')


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'city', 'area', 'address', 'name', 'mobile')
        # exclude = ('owner',)


class ContactSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(source='friend.profile.name')
    nick = serializers.StringRelatedField(source='friend.profile.nick')
    level = serializers.StringRelatedField(source='friend.level')
    avatar = serializers.ImageField(source='friend.profile.avatar', read_only=True)
    userid = serializers.IntegerField(source='friend_id', read_only=True)

    class Meta:
        model = Contact
        fields = ('userid', 'nick', 'name', 'alias', 'black', 'avatar', 'hide', 'status', 'level')


class ContainsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contains
        fields = ('contains',)


class ContactDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('hide', 'black', 'alias')


class ContactHideSerializer(serializers.Serializer):
    userid = serializers.CharField(label='用户ID')

    class Meta:
        fields = ('userid',)


class ContactBlackSerializer(serializers.ModelSerializer):
    userid = serializers.CharField(label='用户ID')

    class Meta:
        fields = ('userid',)


class AccountDetailsSerializer(serializers.ModelSerializer):
    avatar = serializers.ReadOnlyField(source='profile.avatar')
    birthday = serializers.ReadOnlyField(source='profile.birthday')
    nick = serializers.ReadOnlyField(source='profile.nick')
    name = serializers.ReadOnlyField(source='profile.name')
    gender = serializers.ReadOnlyField(source='profile.gender')

    class Meta:
        # depth = 1
        model = get_user_model()
        fields = ('url', 'nick', 'name', 'mobile', 'avatar', 'email', 'birthday', 'gender')

        # read_only_fields = ('email', 'username',)
        extra_kwargs = {
            # 'favorites': {'view_name': 'me-favorites-list', 'lookup_field': 'pk'},
            # 'profile': {'view_name': 'profile-detail', 'lookup_field': 'username', 'read_only': True, 'many': True},
        }


class BankcardSerializer(serializers.ModelSerializer):
    # def validate(self, attrs):
    #     raise serializers.ValidationError("银行卡已存在")

    #     try:
    #         Bankcard.objects.filter(card=attrs.get('card'))
    #         raise serializers.ValidationError("银行卡已存在")
    #     except Bankcard.DoesNotExist:
    #         return attrs

    class Meta:
        model = Bankcard
        exclude = ('owner',)
        read_only_fields = ('cover',)


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        exclude = ('owner',)


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('friend_verify', 'mobile_verify', 'name_public')
