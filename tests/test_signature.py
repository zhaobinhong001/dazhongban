# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model

from service.restauth.models import VerifyCode
from .test_base import BaseAPITestCase


class APITestSignature(BaseAPITestCase):
    """
    Case #1:
    - user profile: defined
    - custom registration: backend defined
    """

    MOBILE = '18742514206'
    VERIFY = '123456'

    def setUp(self):
        self.init()

        owenr = get_user_model()(mobile=self.MOBILE)
        owenr.save()

        self._generate_uid_and_token(user=owenr)

    def test_identity_validation(self):
        payload = {
            "mobile": self.MOBILE
        }

        resp = self.post('/api/auth/registration/verify_mobile/', data=payload, status_code=200)
        self.assertEqual(resp.json['detail'], u'验证码已经成功发送')

        code = VerifyCode.objects.get(mobile=payload['mobile'])

        payload["verify"] = code.code
        resp = self.post('/api/auth/registration/', data=payload, status_code=201)
        self.assertTrue(bool(resp.json.get('key')))
        self.token = resp.json.get('key')

        payload = {
            "certId": "230221198902203010",
            "name": "刘鹏",
            "phone": "13141039522",
            "cardNo": "6227000014150347510",
            "bankID": "CCB",
            "level": "A",
            "frontPhoto": open('assets/media/avatar/default.jpg', 'rb'),
            "backPhoto": open('assets/media/avatar/default.jpg', 'rb'),
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token %s' % self.token)
        resp = self.client.post('/api/sign/identity/', data=payload, format='multipart')
        self.assertEquals(resp.status_code, 200, msg=resp)
        print resp.content

        self.client.credentials(HTTP_AUTHORIZATION='Token %s' % self.token)
        resp = self.client.post('/api/sign/counter/', data={'secret': '1234567890', 'verify': '654321'})
        self.assertEquals(resp.status_code, 200, msg=resp)
        print resp.content

        resp = self.get('/api/me/profile/', status_code=200)
        self.assertEquals(resp.json['level'], 'A')
        self.assertIsNotNone(resp.json['gender'], msg=resp.json['gender'])
        print resp.content

        resp = self.get('/api/me/bankcard/', status_code=200)
        self.assertTrue(resp.json['results'])
