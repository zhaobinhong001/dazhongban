# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import short_url
from rest_framework import viewsets
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from service.consumer.models import Blacklist
from .serializers import (
    AddressSerializer, ProfileSerializer, AvatarSerializer, ContactSerializer, AffairsSerializer, BankcardSerializer, BlacklistSerializer, SettingsSerializer)
from .utils import get_user_profile
from .utils import get_user_settings


#
# class FeedbackViewSet(viewsets.ModelViewSet):
#     queryset = Feedback.objects.all()
#     serializer_class = FeedbackSerializer


class ProfileViewSet(RetrieveUpdateAPIView):
    '''
    用户信息
    '''
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     data = serializer.data
    #     # slug = self.request.user.slug.hex if self.request.user.slug else None
    #     # data['slug'] = short_url.encode_url(instance.pk)
    #     data['qrcode'] = reverse('frontend.views.q', args=[data['slug']], request=request)
    #     return Response(data)

    def get_object(self):
        return get_user_profile(self.request.user)

        #
        # class TradeViewSet(viewsets.ReadOnlyModelViewSet):
        #     '''
        #     这个接口是用来接收APP购买成功后返回的信息.
        #
        #     字段待定...
        #     '''
        #     # queryset = Trade.objects.all()
        #     serializer_class = TradeSerializer
        #     permission_classes = (IsAuthenticated,)
        #
        #     def get_queryset(self):
        #         return self.request.user.trade_set.filter(confirmed__isnull=False)
        # return self.request.user.trade_set.all()


class AvatarViewSet(RetrieveUpdateAPIView):
    '''
    头像上传接口.

    '''
    serializer_class = AvatarSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_user_profile(self.request.user)


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.address_set.all()


# class AffairsViewSet(viewsets.ModelViewSet):
#     serializer_class = AffairsSerializer
#     permission_classes = (IsAuthenticated,)
#
#     def get_queryset(self):
#         return self.request.user.contact_set.all()


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.contact_set.all()


class BankcardViewSet(viewsets.ModelViewSet):
    '''
    银行卡信息
    '''
    serializer_class = BankcardSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.bankcard_set.all()


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


class SettingsViewSet(RetrieveUpdateAPIView):
    '''
    用户设置
    '''
    serializer_class = SettingsSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        # return self.request.user.settings
        return get_user_settings(self.request.user)

