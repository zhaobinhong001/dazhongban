# -*- coding: utf-8 -*-
import json

import requests

from .test_base import BaseAPITestCase


class APITestPassport(BaseAPITestCase):
    """
    Case #1:
    - user profile: defined
    - custom registration: backend defined
    """

    def test_verify_sign(self):
        data = {
            'type': 'payment',
            'data': {
                'req_id': '1213123132',
                'appkey': 'val',
                'uri': '/api/passport/payment/',
                'orderid': '',
            }
        }

        data = json.dumps(data)
        data = requests.post('http://10.7.7.22:9090/Sign', data=data)
        data = data.content.decode('hex')

        data = requests.post('http://10.7.7.22:9090/Verify', data=data)
        print data.content
