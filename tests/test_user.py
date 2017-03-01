# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from .test_base import BaseAPITestCase


class APITestUser(BaseAPITestCase):
    """
    Case #1:
    - user profile: defined
    - custom registration: backend defined
    """
    MOBILE = '15010786971'
    VERIFY = '123456'

    def setUp(self):
        self.init()

        owenr = get_user_model()(mobile=self.MOBILE)
        owenr.save()

        self._generate_uid_and_token(user=owenr)

    def test_user_validation(self):
        data = {
            'type': "invite",
            'data': {
                'uri': "/api/users/12/invite/",
            }
        }

        conten = self.post('/api/users/12/invite/', data=data, status_code=201)

        print conten

    def test_contract_validation(self):
        data = {
            "id": 1,
            "created": "2017-02-24 02:00:15",
            "modified": "2017-02-24 02:00:15",
            "status": "normal",
            "status_changed": "2017-02-24 02:00:15",
            "type": "transfer",
            "mobile": "15010786971",
            "amount": "11.00",
            "summary": "1",
            "make_date": "null",
            "orderid": "1487923215489254455118",
            "payment": "null",
            "receipt": "null",
            "payment_bank": "null",
            "receipt_bank": "null",
        }

        self.post('/api/trade/contract/', data=data, status_code=201)
