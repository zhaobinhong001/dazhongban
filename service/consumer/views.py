# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import short_url
from django.db.models import QuerySet
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

from service.consumer.models import Contact
from .serializers import (
    AddressSerializer, ProfileSerializer, AvatarSerializer, ContactSerializer, BankcardSerializer,
    SettingsSerializer, AddFriendSerializer, NickSerializer)
from .utils import get_user_profile
from .utils import get_user_settings


class ProfileViewSet(RetrieveUpdateAPIView):
    '''
    用户信息
    '''
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['qr'] = reverse('q', args=[short_url.encode_url(instance.pk)], request=request)

        return Response(data)

    def get_object(self):
        return get_user_profile(self.request.user)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class NickViewSet(RetrieveUpdateAPIView):
    '''
    昵称修改接口.

    '''
    serializer_class = NickSerializer
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
    queryset = Contact.objects.all()

    def get_queryset(self):
        queryset = self.queryset.filter(owner=self.request.user).filter(black=False)

        if isinstance(queryset, QuerySet):
            queryset = queryset.all()

        return queryset

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    @detail_route(methods=['get'])
    def addfriend(self, request, pk=None):
        instance, status_ = Contact.objects.get_or_create(friend_id=pk, owner=request.user)

        detail = '成功添加好友' if status_ else '该用户已经是您的好友了'
        return Response({'detail': detail}, status=status.HTTP_200_OK)


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
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset.filter(owner=self.request.user).filter(black=True)

        if isinstance(queryset, QuerySet):
            queryset = queryset.all()

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


class AddFriendViewSet(viewsets.GenericViewSet):
    '''
    用户设置
    '''
    serializer_class = AddFriendSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_user_settings(self.request.user)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
