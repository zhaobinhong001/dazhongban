# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin
from rongcloud import RongCloud

from .models import Groups
from .serializers import GroupsSerializer


class UserViewSet(NestedViewSetMixin, ModelViewSet):
    model = get_user_model()


client = RongCloud(settings.RONGCLOUD_APPKEY, settings.RONGCLOUD_SECRET)


class TokenViewSet(NestedViewSetMixin, ModelViewSet):
    pass


class GroupViewSet(NestedViewSetMixin, mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    '''
    融云群聊接口
    ===========
    链接：
    ----
    - 加入群组: [/api/im/groups/&#60;pk&#62;join/](/api/im/groups/<pk>/join/)

    输入:
    ----
    -  name, 必须, 组名
    -  id, 必须, 组id

    输出:
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
        return serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        result = client.Group.dismiss(userId=self.request.user.pk, groupId=self.request.data.get('id'))
        if not result:
            raise Exception
        instance.delete()

    def perform_update(self, serializer):
        result = client.Group.refresh(groupId=self.request.user.pk, groupName=self.request.data.get('name'))
        if not result:
            raise Exception
        serializer.save()

    @detail_route(methods=['get'])
    def join(self, request, pk=None):
        result = client.Group.join(userId=request.user.pk, groupId=pk, groupName=request.data.get('name'))
        if not result:
            raise Exception
        return Response({'detail': result})

    @detail_route(methods=['get'])
    def dismiss(self, request, pk=None):
        result = client.Group.dismiss(userId=request.pk, groupId=pk)
        if not result:
            raise Exception
        return Response({'detail': result})

    @detail_route(methods=['get'])
    def quit(self, request, pk=None):
        result = client.Group.quit(userId=request.user.pk, groupId=pk)
        if not result:
            raise Exception
        return Response({'detail': result}, status=status.HTTP_200_OK)

    @list_route(methods=['get'])
    def users(self, request, pk=None):
        '''
        融云群聊接口 - 群组用户
        ===========
        '''
        result = client.Group.queryUser(groupId=pk)
        if not result:
            raise Exception
        return Response({'detail': result}, status=status.HTTP_200_OK)

    def get_queryset(self):
        return self.request.user.im_groups.all()
