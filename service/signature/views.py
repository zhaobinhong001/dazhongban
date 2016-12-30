# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import base64
import json
import re

import requests
from django.conf import settings
from django.db.models import QuerySet
from django.http import HttpResponse
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

from service.consumer.models import Bankcard
from service.kernel.contrib.utils.hashlib import md5
from service.kernel.utils.bank_random import bankcard
from service.signature.utils import iddentity_verify, fields, process_verify
from .models import Signature, Identity, Validate
from .serializers import SignatureSerializer, IdentitySerializer, ValidateSerializer, BankcardSerializer, \
    CallbackSerializer, CertificateSerializer


class SignatureViewSet(NestedViewSetMixin, mixins.CreateModelMixin, GenericViewSet):
    '''
    验签接口
    =======

    ### 交易验签:
    - ```转账状态 status = ('', '无状态'), ('agree', '同意'), ('reject', '拒绝')```
    - ```转账类型 type = ('transfer', '转账'),('receiver', '收款'),('thirty', '第三方'),```

    ###合约类型
    - ```合约类型('receipt', '收据'),('borrow', '借条'),('owe', '欠条')```

    ### 所有返回正确的结构为 ：

    - ```{'errors': 0, 'detail': {'uri': uri, 'id': res.id, 'type': type, 'status': status}}```

    ### 失败结构
    - ```{'errors': 1, 'detail': detail}```

    ### 输入说明

    > - 输入内容为一个 `json` 编码后的字符串
    > - json 结构为 {'uri':'', 'data':{'token':token,'type': type ...}}
    > - `data` 里`token`,`type`为必须项，
    > - 状态 `status` 和 `id` 发送时刻不传入
    > - 状态 `status` 和 `id` 接受时刻必须传入

    '''
    serializer_class = SignatureSerializer
    model = Signature

    def get_queryset(self):
        return self.request.user.signatures.all()

    def create(self, request, *args, **kwargs):
        # 验签数据
        resp = requests.post(settings.VERIFY_GATEWAY + '/Verify', data=request.body)

        if (resp.status_code != 200) and (resp.status_code != 500):
            body = resp.content
        else:

            # 解析数据
            sign = resp.content.decode('hex')
            rest = json.loads(sign)

            # 处理数据
            uri = rest.get('uri')
            data = rest.get('data')
            body, user = process_verify(uri, data)

            # 保存数据
            if body['errors'] == '0':
                detail = json.dumps(body['detail']) if isinstance(body['detail'], dict) else body['detail']
                data = {'extra': detail, 'signs': resp.content, 'type': body['detail']['type']}

                serializer = self.get_serializer(data=data)
                serializer.is_valid(raise_exception=True)

                self.request.user = user
                self.perform_create(serializer)

            body = json.dumps(body)

        # 服务签名
        resp = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=body)
        return HttpResponse(resp.content)

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
    '''
    验签记录历史
    ----------
    时间过滤规则：
    在 url 后面加 ?created__range=<start_date>,<end_date>
    例如: ?created__range=2010-01-01,2016-12-31
    '''
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filter_fields = ['created']

    ordering_fields = ('created',)
    ordering = ('id',)

    serializer_class = SignatureSerializer
    permission_classes = (IsAuthenticated,)
    model = Signature

    def get_queryset(self):
        return self.request.user.signatures.all()


class IdentityViewSet(viewsets.ModelViewSet):
    '''
    身份认证接口
    ----------

    - 支持借记卡和贷记卡
    - 贷记卡必须填写 `信用卡背面的末3位数字` 和 `有效期` (按卡片背面一样抄录)
    - 根据不同认证填写认证级别 A,B,C,D

    '''
    permission_classes = (IsAuthenticated,)
    serializer_class = IdentitySerializer
    queryset = Identity.objects.all()

    def create(self, request, *args, **kwargs):
        errors = {}

        if not request.data.get('certId'):
            errors['certId'] = _('身份证不能为空')

        if not request.data.get('name'):
            errors['name'] = _('姓名不能为空')

        if not request.data.get('phone'):
            errors['phone'] = _('电话不能为空')

        if not request.data.get('cardNo'):
            errors['cardNo'] = _('银行卡不能为空')

        certId = re.compile(r'^(\d{6})(\d{4})(\d{2})(\d{2})(\d{3})([0-9]|X)$')

        if not certId.match(request.data.get('certId')):
            errors['certId'] = _('证件号码格式错误')

        mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')

        if not mobile_re.match(request.data.get('phone')):
            errors['phone'] = _('电话格式不正确')

        if len(errors):
            return Response({'detail': errors}, status=status.HTTP_400_BAD_REQUEST)

        item = {}
        items = request.data

        # for k in fields:
        #     if k in ['backPhoto', 'frontPhoto']:
        #         if hasattr(items[k], 'file'):
        #             item[k] = base64.b64encode(items[k].file.getvalue())
        #     else:
        #         if items[k].strip():
        #             item[k] = items.get(k).strip()

        for k, v in items.items():
            if k in fields:
                if k in ['backPhoto', 'frontPhoto']:
                    if hasattr(v, 'file'):
                        item[k] = base64.b64encode(v.file.getvalue())
                else:
                    # if v.strip():
                    item[k] = v

        if request.data.get('expired'):
            expired = request.data.get('expired')
            expired = expired.strip() if expired.strip() else None
            expired = expired.split('/')
            expired = expired[1] + expired[0]
            item['exp_Date'] = expired

        data, status_ = iddentity_verify(item)

        print data

        if not status_:
            raise ValidationError(data)

        data['frontPhoto'] = request.data['frontPhoto']
        data['backPhoto'] = request.data['backPhoto']

        # 判断记录是否存在
        # 存在为更新
        try:
            instance = self.get_queryset().get(owner=request.user)
            serializer = self.get_serializer(instance, data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        except Identity.DoesNotExist:
            # 不存在为创建
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            # 创建时，生成模拟银行卡号
            Bankcard.objects.create(owner=request.user, bank=u'收付宝', card=bankcard(), suffix='', type=u'借记卡', flag='')
            request.user.level = request.data.get('level')
            request.user.credit = '50'
            request.user.save()

        return Response(serializer.data)

    def get_queryset(self):
        queryset = self.queryset.filter(owner=self.request.user)

        if isinstance(queryset, QuerySet):
            queryset = queryset.all()

        return queryset

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class CertificateViewSet(GenericViewSet):
    serializer_class = CertificateSerializer

    def get_queryset(self):
        pass

    def list(self, request, *args, **kwargs):
        return Response([])

    def create(self, request, *args, **kwargs):
        result = requests.post(settings.VERIFY_GATEWAY + '/Query', data=request.data.get('dn'))

        if request.data.get('reissue') and (result.json().get('status') == '4'):
            result = requests.post(settings.VERIFY_GATEWAY + '/Reissue', data=request.data.get('dn'))

        return Response(result.json(), status=status.HTTP_200_OK)


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
        return Response({'detail': u'不支持该方法'})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(serializer.data)
