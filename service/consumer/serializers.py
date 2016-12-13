# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import Address, Profile, Contact, Bankcard, Contains


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class ProfileSerializer(serializers.ModelSerializer):
    level = serializers.StringRelatedField(source='owner.level')
    phone = serializers.StringRelatedField(source='owner.mobile')

    class Meta:
        model = Profile
        # read_only_fields = ("name", "phone", "qr", "level",)
        fields = ("name", "nick", "phone", "avatar", "gender", "birthday", "qr", 'level')


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='profile.name', label=u'姓名')
    nick = serializers.CharField(source='profile.nick', label=u'昵称')
    avatar = serializers.ImageField(source='profile.avatar', label=u'头像')

    class Meta:
        model = get_user_model()
        fields = ('id', 'name', 'nick', 'avatar', 'mobile', 'level')


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
        fields = ('id', 'city', 'area', 'address')
        # exclude = ('owner',)


class ContactSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(source='friend.profile.name')
    nick = serializers.StringRelatedField(source='friend.profile.nick')
    level = serializers.StringRelatedField(source='friend.level')
    avatar = serializers.ImageField(source='friend.profile.avatar', read_only=True)

    class Meta:
        model = Contact
        fields = ('id', 'nick', 'name', 'alias', 'black', 'avatar', 'hide', 'status', 'level')


class ContainsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contains
        fields = ('contains',)


class ContactDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('black', 'alias', 'hide')


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
    class Meta:
        model = Bankcard
        exclude = ('owner',)


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('friend_verify', 'mobile_verify', 'name_public')
