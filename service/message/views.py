# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin
from rongcloud import RongCloud

from .models import Groups
from .serializers import GroupsSerializer


class UserViewSet(NestedViewSetMixin, ModelViewSet):
    model = get_user_model()


client = RongCloud(settings.RONGCLOUD_APPKEY, settings.RONGCLOUD_SECRET)


class GroupViewSet(NestedViewSetMixin, ModelViewSet):
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
        result = client.Group.queryUser(groupId=pk)
        if not result:
            raise Exception
        return Response({'detail': result}, status=status.HTTP_200_OK)

    def get_queryset(self):
        return self.request.user.im_groups.all()
