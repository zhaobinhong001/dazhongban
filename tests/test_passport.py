# -*- coding: utf-8 -*-
from random import randint

from .test_base import BaseAPITestCase


class APITestPassport(BaseAPITestCase):
    """
    Case #1:
    - user profile: defined
    - custom registration: backend defined
    """

    # def test_payment_validation(self):
    #     data = {
    #         'type': 'payment',
    #         'data': {
    #             'req_id': '1213123132',
    #             'appkey': 'val',
    #             'uri': '/api/passport/payment/',
    #             'orderid': '121212',
    #         }
    #     }
    #
    #     data = json.dumps(data)
    #     data = requests.post('http://127.0.0.1:8080/Sign', data=data)
    #     text = data.text.decode('hex')
    #
    #     resp = self.post('/api/passport/payment/', data=text, content_type='application/octet-stream', status_code=200)
    #
    #     data = resp.content.decode('hex')
    #     data = requests.post('http://10.7.7.22:9090/Verify', data=data)
    #
    #     print data.content
    #
    # def test_receive_validation(self):
    #     data = {
    #         'type': 'payment',
    #         'data': {
    #             'req_id': '1213123132',
    #             'appkey': 'val',
    #             'uri': '/api/passport/payment/',
    #             'orderid': '',
    #         }
    #     }
    #
    #     data = json.dumps(data)
    #     data = requests.post('http://127.0.0.1:8080/Sign', data=data)
    #     data = data.content.decode('hex')
    #
    #     resp = self.post('/api/passport/receive/', data=data, content_type='application/octet-stream', status_code=200)
    #
    #     data = resp.content.decode('hex')
    #     data = requests.post('http://10.7.7.22:9090/Verify', data=data)
    #
    #     print data.content
    #
    # def test_refunds_validation(self):
    #     data = {
    #         'type': 'payment',
    #         'data': {
    #             'req_id': '1213123132',
    #             'appkey': 'val',
    #             'uri': '/api/passport/payment/',
    #             'orderid': '',
    #         }
    #     }
    #
    #     data = json.dumps(data)
    #     data = requests.post('http://127.0.0.1:8080/Sign', data=data)
    #     data = data.content.decode('hex')
    #
    #     resp = self.post('/api/passport/refunds/', data=data, content_type='application/octet-stream', status_code=200)
    #
    #     data = resp.content.decode('hex')
    #     data = requests.post('http://10.7.7.22:9090/Verify', data=data)
    #
    #     print data.content

    def test_push_validation(self):
        data = {
            'type': 'receive',
            'data': {
                'req_id': randint(0, 122345),
                'openid': '1315464646465',
                'appkey': 'appkey',
                'uri': '/api/passport/receive/',
                'orders': {
                    'goods': {
                        'title': '',
                        'amount': '',
                        'quantity': '',
                    },
                    'users': {
                        'name': '',
                        'mobile': '',
                        'address': '',
                    },
                    'orderid': '',
                    'created': '',
                    'fee': '',
                    'discount': '',
                    'paymend': '',
                }
            }
        }

        # data = json.dumps(data)
        # data = requests.post('http://127.0.0.1:8080/Sign', data=data)
        # data = data.content.decode('hex')

        resp = self.post('/api/passport/push/', data=data, status_code=200)
        # resp = requests.post('http://10.7.7.22/api/passport/push/', data=data, headers={'content-type': 'application/json'})

        # data = resp.content.decode('hex')
        # data = requests.post('http://10.7.7.22:9090/Verify', data=data)

        print resp.content
