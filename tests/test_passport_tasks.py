# -*- coding: utf-8 -*-
import json

import requests

from .test_base import BaseAPITestCase


class APITestPassportTesk(BaseAPITestCase):
    """
    Case #1:
    - user profile: defined
    - custom registration: backend defined
    """

    # def test_signin_validation(self):
    #     # 登陆假数据
    #     data = {
    #         'type': 'payment',
    #         'data': {
    #             'req_id': '1',
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

    def test_refunds_validation(self):
        # 登陆假数据
        data = {
            'type': 'refunds',
            'data': {
                'req_id': '1',
                'appkey': 'appkey',
                'uri': '/api/passport/refunds/',
                'orderid': '121212',
            }
        }
        data = json.dumps(data)
        data = requests.post('http://10.7.7.22:9090/Sign', data=data)
        data = data.content

        resp = self.post('/api/passport/refunds/', data=data.decode('hex'), content_type='application/octet-stream',
                         status_code=200)
        # 解析数据
        data = resp.content.decode('hex')
        resp = requests.post('http://10.7.7.22:9090/Verify', data=data)

        sign = resp.json()
        try:
            rest = json.loads(sign.get('source').decode('hex').decode('hex'))
        except Exception:
            rest = json.loads(sign.get('source').decode('hex'))
        # 断言第三方返回值是否成功
        self.assertEqual(rest['errors'], 0)


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
