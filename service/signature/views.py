# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import base64

from django.conf import settings
from filters.mixins import FiltersMixin
from rest_framework import filters, mixins, status, viewsets
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin
from url_filter.integrations.drf import DjangoFilterBackend

from service.kernel.contrib.utils.hashlib import md5
from service.signature.utils import iddentity_verify, fields
from .models import Signature, Identity, Validate
from .serializers import SignatureSerializer, IdentitySerializer, ValidateSerializer, BankcardSerializer, \
    CallbackSerializer


class VerifyViewSet(NestedViewSetMixin, mixins.CreateModelMixin, GenericViewSet):
    serializer_class = SignatureSerializer
    permission_classes = (IsAuthenticated,)
    model = Signature

    def get_queryset(self):
        return self.request.user.signatures.all()

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class BankcardViewSet(viewsets.ViewSet):
    serializer_class = BankcardSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        return Response(['serializer.data'], status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class HistoryViewSet(FiltersMixin, ReadOnlyModelViewSet):
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filter_fields = ['created']

    ordering_fields = ('created',)
    ordering = ('id',)

    serializer_class = SignatureSerializer
    permission_classes = (IsAuthenticated,)
    model = Signature

    def get_queryset(self):
        return self.request.user.signatures.all()

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class IdentityViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = IdentitySerializer
    queryset = Identity.objects.all()

    def create(self, request, *args, **kwargs):

        data = request.data

        for k, v in data.items():
            if k in fields:
                if k in ['backPhoto', 'frontPhoto']:
                    if hasattr(v, 'file'):
                        data[k] = base64.b64encode(v.file.getvalue())
                else:
                    data[k] = v

        data = iddentity_verify(request.data)

        if not data:
            raise ValidationError(u"身份认证失败.")

        return Response(data, status=status.HTTP_201_CREATED)

        # serializer = self.get_serializer(data=data)
        # serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        #
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class CallbackViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = CallbackSerializer
    queryset = Validate.objects.all()
    lookup_field = 'nu'

    def create(self, request, *args, **kwargs):
        if not (request.data['key'] == md5(
                    '%s%s%s' % (request.data['nu'], request.data['dn'], settings.IDDENTITY_APPKEY)).hexdigest()):
            raise serializers.ValidationError('key error.')

        instance, _ = Validate.objects.get_or_create(nu=request.data.get('nu'))
        instance.dn = request.data.get('dn')
        instance.key = request.data.get('key')
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ValidateViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ValidateSerializer
    queryset = Validate.objects.all()
    lookup_field = 'nu'

    def list(self, request, *args, **kwargs):
        return Response({'detail':'不支持该方法'})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
