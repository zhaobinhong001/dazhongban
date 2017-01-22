# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import base64
import json

import requests
from django.conf import settings
from django.db.models import QuerySet
from rest_framework import filters, mixins, status, viewsets
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin
from url_filter.integrations.drf import DjangoFilterBackend as drfDjangoFilterBackend

from service.kernel.contrib.utils.hashlib import md5
from service.signature.utils import verify_data, signature_data
from .models import Signature, Identity, Validate, Counter
from .serializers import SignatureSerializer, IdentitySerializer, ValidateSerializer, BankcardSerializer, \
    CallbackSerializer, CertificateSerializer, CounterSerializer
from .tasks import query_sign
from .utils import iddentity_verify, fields, process_verify


class StreamParser(object):
    """
    All parsers should extend `BaseParser`, specifying a `media_type`
    attribute, and overriding the `.parse()` method.
    """
    media_type = '*/*'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Given a stream to read from, return the parsed representation.
        Should return parsed data, or a `DataAndFiles` object consisting of the
        parsed data and files.
        """
        return stream


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
    parser_classes = (StreamParser,)
    model = Signature

    def get_queryset(self):
        return self.request.user.signatures.all()

    def create(self, request, *args, **kwargs):
        # 验签数据
        uri, data = verify_data(request)

        if uri:
            # 处理数据
            body = process_verify(uri, data)
            body = json.dumps(body)
        else:
            body = json.dumps(data)

        # 服务签名
        return signature_data(body)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class BankcardViewSet(viewsets.GenericViewSet):
    serializer_class = BankcardSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class HistoryViewSet(ReadOnlyModelViewSet):
    '''
    验签记录历史
    ----------

    时间过滤规则：
    在 url 后面加 ?created__range={start_date},{end_date}
    例如: ```?created__range=2010-01-01,2016-12-31```
    '''
    filter_backends = (filters.OrderingFilter, filters.DjangoFilterBackend, drfDjangoFilterBackend)
    filter_fields = ('created',)

    ordering_fields = ('created',)
    ordering = ('-created',)

    permission_classes = (IsAuthenticated,)
    serializer_class = SignatureSerializer
    queryset = Signature.objects.all()

    def get_queryset(self):
        queryset = self.queryset.filter(owner=self.request.user)

        if isinstance(queryset, QuerySet):
            queryset = queryset.all()

        return queryset


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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.queryset.filter(owner=self.request.user))
        serializer = self.get_serializer(queryset, many=True)

        try:
            data = serializer.data[0]
            del data['dn']
            del data['expired']
            del data['frontPhoto']
            del data['backPhoto']
        except Exception as e:
            data = serializer.data

        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        try:
            data = serializer.data
            del data['dn']
            del data['expired']
            del data['frontPhoto']
            del data['backPhoto']
        except Exception as e:
            data = serializer.data

        return Response(data)

    def create(self, request, *args, **kwargs):
        # errors = {}

        # if not request.data.get('certId'):
        #     errors['certId'] = _('身份证不能为空')
        #
        # if not request.data.get('name'):
        #     errors['name'] = _('姓名不能为空')
        #
        # if not request.data.get('phone'):
        #     errors['phone'] = _('电话不能为空')
        #
        # if not request.data.get('cardNo'):
        #     errors['cardNo'] = _('银行卡不能为空')
        #
        # certId = re.compile(r'^(\d{6})(\d{4})(\d{2})(\d{2})(\d{3})([0-9]|X)$')
        #
        # if not certId.match(request.data.get('certId')):
        #     errors['certId'] = _('证件号码格式错误')
        #
        # mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
        #
        # if not mobile_re.match(request.data.get('phone')):
        #     errors['phone'] = _('电话格式不正确')

        # if len(errors):
        #     return Response({'detail': errors}, status=status.HTTP_400_BAD_REQUEST)

        if hasattr(request.user, 'identity'):
            if request.user.identity.certId != request.data['certId']:
                raise ValidationError(u'登录的手机号与身份证信息不匹配')

        item = {}
        items = request.data

        for k, v in items.items():
            if k in fields:
                if k in ['backPhoto', 'frontPhoto']:
                    if hasattr(v, 'file'):
                        item[k] = base64.b64encode(v.file.getvalue())
                else:
                    item[k] = v.strip()

        if request.data.get('expired'):
            expired = request.data.get('expired')
            expired = expired.strip() if expired.strip() else None
            expired = expired.split('/')
            expired = expired[1] + expired[0]
            item['exp_Date'] = expired

        data, status_ = iddentity_verify(item)

        if not status_:
            raise ValidationError(data.get('message'))

        data['frontPhoto'] = request.data['frontPhoto']
        data['backPhoto'] = request.data['backPhoto']
        data['bankID'] = request.data['bankID']
        data['level'] = request.data['level']

        if data['level'] == 'A':
            counter, _ = Counter.objects.get_or_create(owner_id=self.request.user.pk)
            counter.secret = '1234567890'
            counter.verify = '654321'
            counter.save()

        self.queryset.filter(owner=self.request.user).delete()

        serializer = self.get_serializer(data=data)
        serializer.is_valid()

        self.perform_create(serializer)

        query_sign(dn=data['dn'], owner=self.request.user)
        return Response(serializer.data)

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


class ValidateViewSet(GenericViewSet):
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


class CounterViewSet(mixins.CreateModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CounterSerializer
    queryset = Counter.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            instance = Counter.objects.get(owner=self.request.user)
            if instance.secret != request.data.get('secret'):
                return Response({'detail': '授权码不正确'}, status=status.HTTP_400_BAD_REQUEST)

            if instance.verify != request.data.get('verify'):
                return Response({'verify': '验证码不正确'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'detail': '验证成功'}, status=status.HTTP_200_OK)
        except Counter.DoesNotExist:
            return Response({'detail': '用户不存在'}, status=status.HTTP_400_BAD_REQUEST)
