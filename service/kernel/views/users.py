# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.filters import FilterSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from service.consumer.serializers import UserSerializer
from ..serializers.report import ReportSerializer


class SearchFilter(FilterSet):
    # min_price = NumberFilter(name="price", lookup_type='gte')
    # max_price = NumberFilter(name="price", lookup_type='lte')

    class Meta:
        model = get_user_model()
        # fields = ['category', 'min_price', 'max_price', 'recommend']
        search_fields = ('profile__nick', 'profile__name', 'mobile')
        # lookup_field = '__all__'


class UsersViewSet(viewsets.ModelViewSet):
    '''
    用户接口
    =======

    - 搜索条件为， 搜索昵称，姓名，以及手机号
    - users/<pk>/report/ 为举报接口

    '''
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('^profile__nick', '^profile__name', 'mobile')

    @detail_route(methods=['POST', 'GET'])
    def report(self, request, pk, *args, **kwargs):
        self.serializer_class = ReportSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
