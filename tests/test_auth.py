# -*- coding: utf-8 -*-

from service.restauth.models import VerifyCode
from .test_base import BaseAPITestCase


class APITestAuth(BaseAPITestCase):
    """
    Case #1:
    - user profile: defined
    - custom registration: backend defined
    """

    MOBILE = '18742514206'
    VERIFY = '123456'

    def setUp(self):
        self.init()

    def test_login_failed_verify_validation(self):
        payload = {
            "mobile": self.MOBILE,
            "verify": self.VERIFY
        }

        resp = self.post('/api/auth/registration/', data=payload, status_code=400)
        self.assertEqual(resp.json['detail'], u'验证码错误.')

    def test_login_null_verify_validation(self):
        payload = {
            "mobile": self.MOBILE,
            "verify": ""
        }

        resp = self.post('/api/auth/registration/', data=payload, status_code=400)
        self.assertEqual(resp.json['detail'], u'验证码不能为空.')

    def test_login_failed_mobile_validation(self):
        payload = {
            "mobile": "",
            "verify": self.VERIFY
        }

        resp = self.post('/api/auth/registration/', data=payload, status_code=400)
        self.assertEqual(resp.json['detail'], u'手机号码不能为空.')

    def test_login_verify_mobile(self):
        payload = {
            "mobile": self.MOBILE
        }

        resp = self.post('/api/auth/registration/verify_mobile/', data=payload, status_code=200)
        self.assertEqual(resp.json['detail'], u'验证码已经成功发送')

        code = VerifyCode.objects.get(mobile=payload['mobile'])
        payload["verify"] = code.code

        resp = self.post('/api/auth/registration/', data=payload, status_code=201)
        self.assertTrue(bool(resp.json.get('key')))
