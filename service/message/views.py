# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin
from rongcloud import RongCloud

from service.consumer.serializers import UserSerializer
from .models import Groups
from .serializers import GroupsSerializer


class UserViewSet(NestedViewSetMixin, ModelViewSet):
    model = get_user_model()


client = RongCloud(settings.RONGCLOUD_APPKEY, settings.RONGCLOUD_SECRET)


class TokenViewSet(GenericViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        nick = request.user.profile.nick if request.user.profile.nick else u'匿名'
        avatar = request.user.profile.avatar if request.user.profile.avatar else u'匿名'
        user = client.User.getToken(userId=request.user.pk, name=nick, portraitUri=avatar)
        data = user.result.get('token')

        return Response({'key': data}, status=status.HTTP_200_OK)


class GroupViewSet(NestedViewSetMixin, mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    '''
    融云群聊接口
    ===========
    相关接口：
    ----
    `pk 为 group 的主键(id)`

    - 创建群组: POST [/api/im/group/](/api/im/group/)
    - 加入群组: GET/POST [/api/im/group/&#60;pk&#62;join/](/api/im/group/<pk>/join/) (GET 请求加自己到群里)
    - 退出群组: GET [/api/im/group/&#60;pk&#62;quit/](/api/im/group/<pk>/quit/)
    - 用户列表: GET [/api/im/group/&#60;pk&#62;users/](/api/im/group/<pk>/users/)
    - 解散群组: GET [/api/im/group/&#60;pk&#62;dismiss/](/api/im/group/<pk>/dismiss/)

    POST 输入:
    ----
    -  name, 必须, 组名
    -  id, 必须, 组id


    异常:
    ----
    `状态码非20x`
    '''
    serializer_class = GroupsSerializer
    permission_classes = (IsAuthenticated,)
    model = Groups

    def perform_create(self, serializer):
        result = client.Group.create(userId=self.request.user.pk, groupId=self.request.data.get('id'),
            groupName=self.request.data.get('name'))

        if not result:
            raise Exception

        result = client.Group.join(userId=self.request.user.pk, groupId=self.request.data.get('id'),
            groupName=self.request.data.get('name'))

        if not result:
            raise Exception

        return serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        result = client.Group.refresh(groupId=self.request.user.pk, groupName=self.request.data.get('name'))

        if not result:
            raise Exception

        serializer.save()

    @detail_route(methods=['POST'])
    def join(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        result = client.Group.join(userId=request.POST['userid'], groupId=pk, groupName=instance.name)

        if not result:
            raise Exception

        return Response({'detail': '您成功加入该群组'}, status=status.HTTP_200_OK)

    @detail_route(methods=['get'])
    def dismiss(self, request, pk=None, *args, **kwargs):
        result = client.Group.dismiss(userId=request.user.pk, groupId=pk)

        if not result:
            raise Exception

        instance = self.get_object()
        self.perform_destroy(instance)

        return Response({'detail': '您成功删除该群组'}, status=status.HTTP_200_OK)

    @detail_route(methods=['get'])
    def quit(self, request, pk=None, *args, **kwargs):
        result = client.Group.quit(userId=request.user.pk, groupId=pk)

        if not result:
            raise Exception

        return Response({'detail': '您成功退出该群组'}, status=status.HTTP_200_OK)

    @detail_route(methods=['get'])
    def users(self, request, pk=None, *args, **kwargs):
        '''
        融云群聊接口 - 群组用户
        ===========
        '''
        result = client.Group.queryUser(groupId=pk)
        userid = [x['id'] for x in result.result.get('users')]
        queryset = get_user_model().objects.filter(id__in=userid)
        self.serializer_class = UserSerializer

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return self.request.user.im_groups.all()
