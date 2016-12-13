# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import short_url
from django.db.models import QuerySet
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import GenericViewSet

from service.consumer.models import Contact
from .serializers import (
    AddressSerializer, ProfileSerializer, AvatarSerializer, ContactSerializer, BankcardSerializer,
    SettingsSerializer, AddFriendSerializer, NickSerializer, ContactDetailSerializer, ContainsSerializer)
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


class ContactViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
    mixins.ListModelMixin, GenericViewSet):
    '''
    联系人接口
    --------

    - 上传通讯录 POST /api/me/contains/
    - 设置黑名单 POST /api/me/contact/{pk}/


    '''
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

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = ContactDetailSerializer
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @list_route(methods=['GET', 'POST'])
    def contains(self, request, *args, **kwargs):
        '''
        [
            {
                "name": "BellKate",
                "phoneNum": [
                    "(555) 564-8583",
                    "(415) 555-3695"
                ]
            },
            {
                "name": "BellKate",
                "phoneNum": [
                    "(555) 564-8583",
                    "(415) 555-3695"
                ]
            },
        ]

        '''
        self.serializer_class = ContainsSerializer
        detail = '成功'
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
    -----

    - 取消黑名单 POST /api/me/blacklist/{pk}
    - POST参数: black = false


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

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = ContactDetailSerializer
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class SettingsViewSet(RetrieveUpdateAPIView):
    '''
    用户设置
    '''
    serializer_class = SettingsSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_user_settings(self.request.user)


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
