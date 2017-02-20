# -*- coding: utf-8 -*-
import requests
from django.conf import settings
from django.contrib.auth import get_user_model

from .test_base import BaseAPITestCase


class APITestDoctor(BaseAPITestCase):
    """
    Case #1:
    - user profile: defined
    - custom registration: backend defined
    """

    MOBILE = '18742514206'

    def setUp(self):
        self.init()

        owenr = get_user_model()(mobile=self.MOBILE)
        owenr.save()

        self._generate_uid_and_token(user=owenr)

    def test_bankcard_validation(self):
        payload = {"card": "6227000014150347510"}

        resp = requests.post(settings.BANK_CARD, data=payload)
        self.assertEquals(resp.status_code, 200)

    def test_verify_signature_validation(self):
        payload = "6227000014150347510"

        resp = requests.post('%s/Sign' % settings.VERIFY_GATEWAY, data=payload)
        self.assertEquals(resp.status_code,200)
        # requests.post('%s/Verify' % settings.VERIFY_GATEWAY, data=resp)
