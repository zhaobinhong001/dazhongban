# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model

from service.signature.models import Signature
from service.trade.models import Contract
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
            "status": "normal",
            "type": "owe",
            "mobile": "15010786971",
            "amount": "11.00",
            "summary": "1",
        }

        self.post('/api/trade/contract/', data=data, status_code=201)

        a = Contract.objects.filter(id=1)
        for a in a:
            print a.status
            print a.type

        print 333333333333333333333333333333333333333333333333333333333

        b = Signature.objects.all()
        for b in b:
            print b.type
            print b.owner
            print b.extra
            print b.signs
            print b.serial
            print b.expired

        self.get('/api/sign/history/', status_code=200)
        print 333333333333333333333333333333333333333333333333333333333
        c = Signature.objects.all()
        for c in c:
            print c.type
            print c.owner
            print c.extra
            print c.signs
            print c.serial
            print c.expired
