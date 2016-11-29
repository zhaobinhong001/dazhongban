# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from service.consumer.models import Blacklist
from .serializers import (
    AddressSerializer, ProfileSerializer, AvatarSerializer, ContactSerializer, BankcardSerializer, BlacklistSerializer,
    SettingsSerializer)
from .utils import get_user_profile
from .utils import get_user_settings


class ProfileViewSet(RetrieveUpdateAPIView):
    '''
    用户信息
    '''
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_user_profile(self.request.user)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class AvatarViewSet(RetrieveUpdateAPIView):
    '''
    头像上传接口.

    '''
    serializer_class = AvatarSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_user_profile(self.request.user)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.address_set.all()

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.contact_set.all()

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class BankcardViewSet(viewsets.ModelViewSet):
    '''
    银行卡信息
    '''
    serializer_class = BankcardSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.bankcard_set.all()

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class BlacklistViewSet(viewsets.ModelViewSet):
    '''
    黑名单
    '''
    queryset = Blacklist.objects.filter(id__gt=1)
    serializer_class = BlacklistSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset.filter(owner=self.request.user)
        return queryset

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class SettingsViewSet(RetrieveUpdateAPIView):
    '''
    用户设置
    '''
    serializer_class = SettingsSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_user_settings(self.request.user)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
