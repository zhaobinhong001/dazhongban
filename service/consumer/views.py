# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import short_url
from django.contrib.auth import get_user_model
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
from service.consumer.models import CustomUser
from .serializers import (
    AddressSerializer, ProfileSerializer, AvatarSerializer, ContactSerializer, BankcardSerializer,
    SettingsSerializer, AddFriendSerializer, NickSerializer, ContactDetailSerializer, ContainsSerializer,
    ContactHideSerializer)
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

    - 上传通讯录 POST /api/me/contact/contains/
    - 设置黑名单 POST /api/me/contact/{pk}/
    - 批量隐藏我名字(批量) POST /api/me/contact/black/
    - 批量隐藏我名字 POST /api/me/contact/hide/
    - 批量黑名单 POST /api/me/contact/black/

    `hide 和 black 接口 psot 参数 userid 为多个 id 用 "," 隔开`


    '''
    serializer_class = ContactSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Contact.objects.all()
    lookup_field = 'friend_id'

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
    def hide(self, request, *args, **kwargs):
        self.serializer_class = ContactHideSerializer
        if request.method == 'POST':
            userid = request.data['userid'].replace(u'，', '.')
            Contact.objects.filter(friend__in=userid.split(','), owner=request.user).update(hide=True)
            return Response({'detail': '成功'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': '不支持 GET 方法'}, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['GET', 'POST'])
    def black(self, request, *args, **kwargs):
        self.serializer_class = ContactHideSerializer
        if request.method == 'POST':
            userid = request.data['userid'].replace(u'，', '.')
            Contact.objects.filter(friend__in=userid.split(','), owner=request.user).update(black=True)
            return Response({'detail': '成功'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': '不支持 GET 方法'}, status=status.HTTP_400_BAD_REQUEST)

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
        # # 解析数据
        contains = request.data.get('contains')
        try:
            contains = json.loads(contains)
        except Exception as e:
            return Response({'detail': 'JSON格式错误'}, status=status.HTTP_400_BAD_REQUEST)

        # 取出所有手机号
        mobiles = []
        contact = {}

        for contain in contains:
            if contain.get('phoneNum'):
                for phone in contain.get('phoneNum'):
                    mobiles.append(phone)
                    contact[phone] = contain.get('name')

        mobiles = list(set(mobiles))

        # 读取数据库里的含税含有手机号列表的数据
        detail = '通讯录没有变化'

        try:
            users = get_user_model().objects.filter(mobile__in=mobiles)

            for user in users:
                obj, st = Contact.objects.get_or_create(owner=self.request.user, friend=user)

                if st:
                    obj.alias = contact[user.mobile]
                    obj.status = 'new'
                    obj.save()

            detail = '通讯录更新成功'
        except CustomUser.DoesNotExist:
            pass

        return Response({'detail': detail}, status=status.HTTP_200_OK)


class BankcardViewSet(viewsets.ModelViewSet):
    '''
    银行卡信息

    银行代码表，已经发送至各位邮件了

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

    - 取消黑名单(批量) POST /api/me/blacklist/revert/
    - 取消黑名单(单个) POST /api/me/blacklist/{pk}
    - POST参数: black = false

    `hide 和 black 接口 psot 参数 userid 为多个 id 用 "," 隔开`
    '''
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'friend_id'

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

    @list_route(methods=['GET', 'POST'])
    def revert(self, request, *args, **kwargs):
        self.serializer_class = ContactHideSerializer
        if request.method == 'POST':
            userid = request.data['userid'].replace(u'，', '.')
            Contact.objects.filter(friend__in=userid.split(','), owner=request.user).update(black=False)
            return Response({'detail': '成功'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': '不支持 GET 方法'}, status=status.HTTP_400_BAD_REQUEST)


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
