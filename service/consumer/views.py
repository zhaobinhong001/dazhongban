# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    AddressSerializer, ProfileSerializer, AvatarSerializer, ContactSerializer)
from .utils import get_user_profile


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

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


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

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
