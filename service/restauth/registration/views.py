# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
import re

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from service.restauth.models import VerifyCode
from service.restauth.registration.utils import GenPassword
from .forms import SignupForm
from .tasks import send_verify_code
from ..serializers import RegisterSerializer, VerifyMobileSerializer
from ..settings import TokenSerializer


class RegisterView(GenericAPIView):
    '''
    注意：

    手机注册前，先请求 `/auth/registration/verify_mobile/` 接口, 获取 verify code.

    请使用下面的正则表达式验证手机号码正确性，在提交服务器前客户端提交一次
    手机号码验证正则表达式：^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$
    '''
    token_model = Token
    form_class = SignupForm
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    response_serializer = TokenSerializer
    queryset = get_user_model().objects.all()
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def form_valid(self, form):
        self.user = form.save(self.request)
        self.token, created = self.token_model.objects.get_or_create(user=self.user)
        return self.token

    def post(self, request, *args, **kwargs):
        self.form = self.form_class(request.data)

        if self.form.is_valid():
            self.form_valid(self.form)
            return self.get_response()
        else:
            return self.get_response_with_errors()

    def get_response(self):
        serializer = self.response_serializer(instance=self.token)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_response_with_errors(self):
        return Response(self.form.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyMobileView(GenericAPIView):
    '''
    注意：

    请使用下面的正则表达式验证手机号码正确性，在提交服务器前客户端提交一次
    手机号码验证正则表达式：^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$
    '''
    response_serializer = TokenSerializer
    permission_classes = (AllowAny,)
    serializer_class = VerifyMobileSerializer
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def post(self, request, *args, **kwargs):
        mobile = request.data.get('mobile')

        # 判断手机是否为空
        if not mobile:
            raise ValidationError({'mobile': "手机号码不能为空."})

        # 判断手机是否匹配规格
        if not re.match(r'^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$', mobile):
            raise ValidationError({'mobile': "手机号码格式不匹配."})

        # 生成验证码
        code = GenPassword(4)

        # 保存数据库
        obj, _ = VerifyCode.objects.get_or_create(mobile=mobile)
        obj.code = code
        obj.save()

        # 发送验证码
        msg = u' 短信验证码  %s 【收付宝科技】' % code
        send_verify_code.delay(mobile, msg)

        # 返回接口
        return Response({'detail': u'验证码已经成功发送'}, status=status.HTTP_200_OK)
