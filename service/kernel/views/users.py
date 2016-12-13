# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings

from service.consumer.models import Contact
from service.consumer.serializers import UserSerializer
from ..serializers.report import ReportSerializer


class UsersViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    用户接口
    =======

    - 搜索条件为， 搜索昵称，姓名，以及手机号
    - users/{pk}/report/ 为举报接口
    - users/{pk}/invite/ 邀请加好友
    - users/{pk}/confirm/ 邀请好友确认

    '''
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('^profile__nick', '^profile__name', 'mobile')

    def perform_report(self, serializer, pk):
        serializer.save(defendant_id=pk, revelator=self.request.user)

    def get_success_headers(self, data):
        try:
            return {'Location': data[api_settings.URL_FIELD_NAME]}
        except (TypeError, KeyError):
            return {}

    def get_queryset(self):
        queryset = self.queryset

        if isinstance(queryset, QuerySet):
            queryset = queryset.exclude(id=self.request.user.pk)

        return queryset

    @detail_route(methods=['POST', 'GET'])
    def report(self, request, pk, *args, **kwargs):
        self.serializer_class = ReportSerializer

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_report(serializer, pk)
        headers = self.get_success_headers(serializer.data)

        return Response({'detail': '操作成功'}, status=status.HTTP_201_CREATED, headers=headers)

    @detail_route(methods=['POST', 'GET'])
    def invite(self, request, pk, *args, **kwargs):
        owner = request.user
        friend = get_user_model().objects.get(id=pk)
        ret, _ = Contact.objects.get_or_create(owner_id=owner.pk, friend_id=friend.pk)

        return Response({'detail': '操作成功'}, status=status.HTTP_201_CREATED)

    @detail_route(methods=['POST', 'GET'])
    def confirm(self, request, pk, *args, **kwargs):
        owner = request.user
        friend = get_user_model().objects.get(id=pk)
        ret = Contact.objects.filter(owner_id=owner.pk, friend_id=friend.pk)

        if ret:
            ret.status = 'confirm'
            ret.save()
            return Response({'detail': '操作成功'}, status=status.HTTP_201_CREATED)

        return Response({'detail': '操作失败'}, status=status.HTTP_400_BAD_REQUEST)
