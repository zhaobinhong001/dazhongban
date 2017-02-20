# coding:utf-8
from __future__ import unicode_literals
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from bank.models import Banklog
from django.conf import settings


@csrf_exempt
def BankViewSet(request, *args, **kwargs):
    if request.method == "POST":

        # 验签数据
        resp = requests.post(settings.VERIFY_GATEWAY + '/Verify', data=request)

        # 解析数据
        sign = resp.json()
        if (resp.status_code != 200) and (resp.status_code != 500):
            third = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=resp.content)
            return HttpResponse(third.content)

        try:
            rest = json.loads(sign.get('source').decode('hex').decode('hex'))
        except Exception:
            rest = json.loads(sign.get('source').decode('hex'))

        # 保存日志

        Banklog.objects.create(receive=rest['data']['receive'], orderid=rest['data']['orderid'],
                               amount=rest['goods']['amount'], title=rest['goods']['title'])

        content = json.dumps({'type': 'payment',
                              'data': {
                                  'errors': 0,
                                  'detail': '支付成功',
                                  'req_id': '1',
                                  'appkey': 'appkey',
                                  'uri': '/api/passport/payment/',
                                  'orderid': '121212',
                              }})

        third = requests.post(settings.VERIFY_GATEWAY + '/Sign', data=content)

        return HttpResponse(third.content.decode('hex'))
