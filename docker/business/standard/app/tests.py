# coding:utf-8
import os
import three
import unittest
import tempfile
import requests

from flask import jsonify

SIGNUPDATA = '{"data": {"appkey": "appkey", "uri": "/api/passport/signup/", "req_id": "c51ce410c124a10e0db5e4b97fc2af39"}, "type": "signup"}'
SIGNNINDATA = '{"data": {"appkey": "appkey", "uri": "/api/passport/signin/", "req_id": "c51ce410c124a10e0db5e4b97fc2af39"}, "type": "signin"}'
PAYMENTDATA = '{"data": {"appkey": "appkey", "uri": "/api/passport/payment/", "req_id": "c51ce410c124a10e0db5e4b97fc2af39"}, "type": "payment"}'
RECEIVEDATA = '{"data": {"appkey": "appkey", "uri": "/api/passport/receive/", "req_id": "c51ce410c124a10e0db5e4b97fc2af39"}, "type": "receive"}'
REFUNDSDATA = '{"data": {"appkey": "appkey", "uri": "/api/passport/refunds/", "req_id": "c51ce410c124a10e0db5e4b97fc2af39"}, "type": "refunds"}'

VERIFY = 'http://10.7.7.22:9090'


class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, three.app.config['DATABASE'] = tempfile.mkstemp()

        three.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + three.app.config['DATABASE']
        three.app.config['TESTING'] = True

        self.app = three.app.test_client()
        three.init_db()

        print three.app.config['SQLALCHEMY_DATABASE_URI']

        self.init_data()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(three.app.config['DATABASE'])

    def init_data(self):
        pass

    # 注册
    def test_signup(self):
        resp = requests.post(VERIFY + '/Sign', data=SIGNUPDATA)
        assert resp.status_code == 200

        status = self.app.post('/services/callback/signup', data=resp.content.decode('hex'))
        req_status = status.get_data()

        from three import Sign
        print Sign.query.all()

        print req_status

        assert status.status_code == 200
        # assert status is not None

    # 登录
    def test_signin(self):
        resp = requests.post(VERIFY + '/Sign', data=SIGNNINDATA)
        assert resp.status_code == 200
        status = self.app.post('/services/callback/signin', data=resp.content.decode('hex'))
        req_status = status.get_data()
        print req_status
        assert status.status_code == 200

    # 支付
    def test_payment(self):
        resp = requests.post(VERIFY + '/Sign', data=PAYMENTDATA)
        assert resp.status_code == 200
        status = self.app.post('/services/callback/payment', data=resp.content.decode('hex'))
        req_status = status.get_data()
        print req_status
        assert status.status_code == 200

    # 收货
    def test_receive(self):
        resp = requests.post(VERIFY + '/Sign', data=RECEIVEDATA)
        assert resp.status_code == 200
        status = self.app.post('/services/callback/receive', data=resp.content.decode('hex'))
        req_status = status.get_data()
        print req_status
        assert status.status_code == 200

    # 退货
    def test_refunds(self):
        resp = requests.post(VERIFY + '/Sign', data=REFUNDSDATA)
        assert resp.status_code == 200
        status = self.app.post('/services/callback/refunds', data=resp.content.decode('hex'))
        req_status = status.get_data()
        print req_status
        assert status.status_code == 200


if __name__ == '__main__':
    unittest.main()
