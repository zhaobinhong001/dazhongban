# -*- coding: utf-8 -*-
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

        self.post('/api/sign/bankcard/', data=payload, status_code=201)

    def test_verify_signature_validation(self):
        payload = "6227000014150347510"

        resp = self.post('%s/Sign' % settings.VERIFY_GATEWAY, data=payload, status_code=200)
        self.post('%s/Verify' % settings.VERIFY_GATEWAY, data=resp, status_code=200)
