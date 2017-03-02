# -*- coding: utf-8 -*-
import requests
from django.contrib.auth import get_user_model

from .test_base import BaseAPITestCase


class APITestVerify(BaseAPITestCase):
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

    # def test_verify_validation(self):
    #     data = open('/Users/bopo/tmp/verify.txt').read()
    #     resp = self.post('/api/sign/signature/', data=data, content_type='application/x-www-form-urlencoded', status_code=200)
    #     resp = self.post('/api/sign/signature/', data=data, content_type='application/octet-stream', status_code=200)
    #     resp = requests.post('http://10.7.7.22:9090/Verify', data=resp.content.decode('hex'))
    #
    #     print resp.content