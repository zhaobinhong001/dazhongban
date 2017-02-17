# -*- coding: utf-8 -*-
import json

import requests

from django.contrib.auth import get_user_model

from service.passport.models import WaterLog
from .test_base import BaseAPITestCase


class APITestPassportTesk(BaseAPITestCase):
    """
    Case #1:
    - user profile: defined
    - custom registration: backend defined
    """
    MOBILE = '15010786971'
    VERIFY = '123456'

    def setUp(self):
        self.init()

        self.owenr = get_user_model()(mobile=self.MOBILE)
        self.owenr.save()

        self.log = WaterLog.objects.create(appkey='appkey', owner=self.owenr)

        self._generate_uid_and_token(user=self.owenr)

    # def test_payment_validation(self):
    #     # 支付
    #     data = {
    #         'type': 'payment',
    #         'data': {
    #             'req_id': '1',
    #             'openid': '123456',
    #             'appkey': 'appkey',
    #             'uri': '/api/passport/payment/',
    #             'orderid': '121212',
    #         }
    #     }
    #     data = json.dumps(data)
    #     data = requests.post('http://10.7.7.22:9090/Sign', data=data)
    #     data = data.content
    #
    #     resp = self.post('/api/passport/payment/', data=data.decode('hex'), content_type='application/octet-stream',
    #                      status_code=200)
    #     # 解析数据
    #     data = resp.content.decode('hex')
    #     resp = requests.post('http://10.7.7.22:9090/Verify', data=data)
    #
    #     sign = resp.json()
    #     try:
    #         rest = json.loads(sign.get('source').decode('hex').decode('hex'))
    #     except Exception:
    #         rest = json.loads(sign.get('source').decode('hex'))
    #     # 断言第三方返回值是否成功
    #     self.assertEqual(rest['errors'], 0)
    #
    # def test_receive_validation(self):
    #     # 收货
    #     data = {
    #         'type': 'receive',
    #         'data': {
    #             'req_id': '2',
    #             'openid': '123456',
    #             'appkey': 'appkey',
    #             'uri': '/api/passport/receive/',
    #             'orderid': '121212',
    #         }
    #     }
    #     data = json.dumps(data)
    #     data = requests.post('http://10.7.7.22:9090/Sign', data=data)
    #     data = data.content
    #
    #     # self.client.credentials(HTTP_AUTHORIZATION='Token %s' % self.token)
    #     resp = self.post('/api/passport/receive/', data=data.decode('hex'), content_type='application/octet-stream',
    #                      status_code=200)
    #
    #     # 解析数据
    #     data = resp.content.decode('hex')
    #     resp = requests.post('http://10.7.7.22:9090/Verify', data=data)
    #
    #     sign = resp.json()
    #     try:
    #         rest = json.loads(sign.get('source').decode('hex').decode('hex'))
    #     except Exception:
    #         rest = json.loads(sign.get('source').decode('hex'))
    #     # 断言是否成功
    #     self.assertEqual(rest['errors'], 0)
    #     print rest
    #
    # def test_signin_validation(self):
    #     # 登陆
    #     data = {
    #         'type': 'signin',
    #         'data': {
    #             'req_id': '2',
    #             'openid': '123456',
    #             'appkey': 'appkey',
    #             'uri': '/api/passport/signin/',
    #             'orderid': '121212',
    #         }
    #     }
    #     data = json.dumps(data)
    #     data = requests.post('http://10.7.7.22:9090/Sign', data=data)
    #     data = data.content
    #
    #     # self.client.credentials(HTTP_AUTHORIZATION='Token %s' % self.token)
    #     resp = self.post('/api/passport/signin/', data=data.decode('hex'), content_type='application/octet-stream',
    #                      status_code=200)
    #
    #     # 解析数据
    #     data = resp.content.decode('hex')
    #     resp = requests.post('http://10.7.7.22:9090/Verify', data=data)
    #
    #     sign = resp.json()
    #     try:
    #         rest = json.loads(sign.get('source').decode('hex').decode('hex'))
    #     except Exception:
    #         rest = json.loads(sign.get('source').decode('hex'))
    #     # 断言是否成功
    #     self.assertEqual(rest['errors'], 0)
    #     print rest
    #
    # def test_signup_validation(self):
    #     # 注册
    #     data = {
    #         'type': 'signup',
    #         'data': {
    #             'req_id': '2',
    #             'openid': '123456',
    #             'appkey': 'appkey',
    #             'uri': '/api/passport/signup/',
    #             'orderid': '121212',
    #         }
    #     }
    #     data = json.dumps(data)
    #     data = requests.post('http://10.7.7.22:9090/Sign', data=data)
    #     data = data.content
    #
    #     # self.client.credentials(HTTP_AUTHORIZATION='Token %s' % self.token)
    #     resp = self.post('/api/passport/signup/', data=data.decode('hex'),
    #                      content_type='application/octet-stream',
    #                      status_code=200)
    #
    #     # 解析数据
    #     data = resp.content.decode('hex')
    #     resp = requests.post('http://10.7.7.22:9090/Verify', data=data)
    #
    #     sign = resp.json()
    #     try:
    #         rest = json.loads(sign.get('source').decode('hex').decode('hex'))
    #     except Exception:
    #         rest = json.loads(sign.get('source').decode('hex'))
    #     # 断言是否成功
    #     self.assertEqual(rest['errors'], 0)
    #     print rest
    #
    # def test_refunds_validation(self):
    #     # 退货
    #     data = {
    #         'type': 'refunds',
    #         'data': {
    #             'req_id': '2',
    #             'openid': '123456',
    #             'appkey': 'appkey',
    #             'uri': '/api/passport/refunds/',
    #             'orderid': '121212',
    #         }
    #     }
    #     data = json.dumps(data)
    #     data = requests.post('http://10.7.7.22:9090/Sign', data=data)
    #     data = data.content
    #
    #     # self.client.credentials(HTTP_AUTHORIZATION='Token %s' % self.token)
    #     resp = self.post('/api/passport/refunds/', data=data.decode('hex'),
    #                      content_type='application/octet-stream',
    #                      status_code=200)
    #
    #     # 解析数据
    #     data = resp.content.decode('hex')
    #     resp = requests.post('http://10.7.7.22:9090/Verify', data=data)
    #
    #     sign = resp.json()
    #     try:
    #         rest = json.loads(sign.get('source').decode('hex').decode('hex'))
    #     except Exception:
    #         rest = json.loads(sign.get('source').decode('hex'))
    #     # 断言是否成功
    #     self.assertEqual(rest['errors'], 0)
    #     print rest

    def test_push_validation(self):
        data = {
            'type': 'receive',
            'data': {
                'req_id': '请求唯一的id, 发起方随机生成',
                'appkey': '系统分配给商家的唯一标示',
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

        data = json.dumps(data)
        # data = requests.post('http://127.0.0.1:8080/Sign', data=data)
        # data = data.content.decode('hex')

        # resp = self.post('/api/passport/push/', data=data, status_code=200)
        resp = self.post('/api/passport/pussh/', data=data,
                         content_type='application/octet-stream',
                         status_code=200)

        # data = resp.content.decode('hex')
        # data = requests.post('http://10.7.7.22:9090/Verify', data=data)

        print resp.content

        # resp = requests.post(url='http://10.7.7.224:3000/services/callback/signin', data=data)
        # data1 = {
        #     'enterprise_name': '工商银行',
        #     'bank_accountType': '工商银行',
        #     'bank_accountName': '工商银行',
        #     'bank_num': '62123456464654564',
        #     'bank_account': '工商银行',
        #     'bank_add': '工商银行',
        #     'bank_branch': '工商银行',
        #     'yesterday_income': '11111',
        #     'platform_income': '1111111',
        #     'settled_date': '1486569600000',
        #     'appkey': 'appkey',
        #     'secret': '111',
        #     'callback': 'http://10.7.7.47:3000/api/passport/signin',
        # }
        #
        # EnterpriseUser.objects.create(**data1)

        # def test_third_validation(self):
        #     data = {
        #         'type': 'signin',
        #         'data': {
        #             'req_id': '1',
        #             'appkey': 'appkey',
        #             'uri': '/api/passport/signin/',
        #             'orderid': '121212',
        #         }
        #     }
        #
        #     data = json.dumps(data)
        #     data = requests.post('http://10.7.7.22:9090/Sign', data=data)
        #     data = data.content.decode('hex')
        #
        #     resp = self.post('http://10.7.7.47:3000/services/callback/signin', data=data, content_type='application/octet-stream', status_code=200)
        #
        #     data = resp.content.decode('hex')
        #     data = requests.post('http://10.7.7.22:9090/Verify', data=data)
        #
        #     print data.content
