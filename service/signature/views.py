# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import base64
import re

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
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

    def create(self, request, *args, **kwargs):
        print request.data.get('signs')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class BankcardViewSet(viewsets.GenericViewSet):
    serializer_class = BankcardSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
        errors = {}

        if not request.data.get('certId'):
            errors['certId'] = _('姓名不能为空')

        if not request.data.get('name'):
            errors['name'] = _('姓名不能为空')

        if not request.data.get('phone'):
            errors['phone'] = _('电话不能为空')

        if not request.data.get('cardNo'):
            errors['cardNo'] = _('银行卡不能为空')

        if not request.data.get('certId'):
            errors['certId'] = _('姓名不能为空')

        if not request.data.get('backPhoto'):
            errors['backPhoto'] = _('姓名不能为空')

        certId = re.compile(r'^(\d{6})(\d{4})(\d{2})(\d{2})(\d{3})([0-9]|X)$')

        if not certId.match(request.data.get('certId')):
            errors['certId'] = _('证件号码格式错误')

        mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')

        if not mobile_re.match(request.data.get('phone')):
            errors['phone'] = _('电话格式不正确')

        cardNo = re.compile(r'^(\d{16}|\d{19})$')
        if not cardNo.match(request.data.get('cardNo')):
            errors['carNo'] = _('银行卡格式不正确')

        if len(errors):
            return Response({'detail': errors}, status=status.HTTP_400_BAD_REQUEST)

        item = {}
        items = request.data

        for k, v in items.items():
            if k in fields:
                if k in ['backPhoto', 'frontPhoto']:
                    if hasattr(v, 'file'):
                        item[k] = base64.b64encode(v.file.getvalue())
                else:
                    if v.strip():
                        item[k] = v

        if request.data.get('expired'):
            expired = request.data.get('expired')
            expired = expired.strip() if expired.strip() else None
            expired = expired.split('/')
            expired = expired[1] + expired[0]
            item['exp_Date'] = expired

        data, status_ = iddentity_verify(item)

        if not status_:
            raise ValidationError(data)

        return Response(data, status=status.HTTP_201_CREATED)

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
        return Response({'detail': '不支持该方法'})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(serializer.data)
