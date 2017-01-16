# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from .test_base import BaseAPITestCase


class APITestme(BaseAPITestCase):
    """
    Case #1: 用户地址
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

    def test_post_request_address(self):
        payload = {
            "mobile": "15710002821",
            "city": "北京",
            "address": "234112",
            "name": "21345",
            "area": "134"
        }
        self.post('/api/me/address/', data=payload, status_code=201)

    def test_get_request_address(self):
        self.get('/api/me/address/', status_code=200)

    def test_patch_request_address(self):
        payload = {
            "mobile": "15710002821",
            "city": "北京",
            "address": "234112",
            "name": "21345",
            "area": "134"
        }
        self.post('/api/me/address/', data=payload, status_code=201)

        payload1 = {
            "mobile": "15710002822",
        }
        self.patch('/api/me/address/1/', data=payload1, status_code=200)

    def test_put_request_address(self):
        payload = {
            "mobile": "15710002821",
            "city": "北京",
            "address": "234112",
            "name": "21345",
            "area": "134"
        }
        self.post('/api/me/address/', data=payload, status_code=201)

        payload2 = {
            "mobile": "15710002823",
            "city": "北京",
            "address": "234112",
            "name": "21345",
            "area": "134"
        }
        self.put('/api/me/address/1/', data=payload2, status_code=200)

    def test_delete_request_address(self):
        payload = {
            "mobile": "15710002821",
            "city": "北京",
            "address": "234112",
            "name": "21345",
            "area": "134"
        }
        self.post('/api/me/address/', data=payload, status_code=201)

        self.delete('/api/me/address/1/', status_code=204)

    def test_get_request_avatar(self):
        self.get('/api/me/avatar/', status_code=200)

    def test_get_request_nick(self):
        self.get('/api/me/nick/', status_code=200)

    def test_patch_request_nick(self):
        payload = {
            "nick": "2134"
        }
        result1 = self.client.patch('/api/me/nick/', data=payload, status_code=200)
        print result1.json
