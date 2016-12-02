# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from .models import Groups, Token


class GroupsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Groups
        fields = ('id', 'name',)


class UsersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Groups
        fields = ('id', 'name',)


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        exclude = ('owner','id')
