# -*- coding: utf-8 -*-
import sys

import jpush as jpush
# import top
from django.conf import settings
from jinja2 import Template

reload(sys)
sys.setdefaultencoding('utf8')


def response(jsonobj, key):
    obj = jsonobj.get(key)
    suc = False

    if obj:
        success = obj.get('result').get('successful')

        if success is True:
            suc = True

        msg = obj.get('result').get('message')
    else:
        msg = obj.get('error_response').get('sub_msg')

    return [suc, msg]


def send_verify_code(mobile):
    pass
    # req = top.api.OpenSmsSendvercodeRequest()
    # req.set_app_info(top.appinfo(settings.TOP_APPKEY, settings.TOP_SECRET))
    # req.send_ver_code_request = {'mobile': int(mobile)}

    # try:
    #     resp = req.getResponse()
    #     return response(resp, 'open_sms_sendvercode_response')
    # except Exception, e:
    #     print(e)
    #     return False


def check_verify_code(mobile, verify):
    psaa
    # req = top.api.OpenSmsCheckvercodeRequest()
    # req.set_app_info(top.appinfo(settings.TOP_APPKEY, settings.TOP_SECRET))
    # req.check_ver_code_request = {'mobile': int(mobile), 'ver_code': int(verify)}

    # try:
    #     resp = req.getResponse()
    #     return response(resp, 'open_sms_checkvercode_response')
    # except Exception, e:
    #     raise e


def get_itmes(keyword, page_size):
    FIELDS = "open_iid,coupon_price,open_iid,title,nick,pic_url,price,commission,commission_rate,commission_num," \
             "commission_volume,seller_credit_score,item_location,volume"
    inf = top.appinfo(settings.TOP_APPKEY, settings.TOP_SECRET)
    req = top.api.AtbItemsGetRequest()

    req.set_app_info(inf)
    req.fields = FIELDS
    req.keyword = keyword.decode('utf8')
    req.page_size = page_size

    try:
        resp = req.getResponse()
        return response(resp, 'atb_items_get_response')
    except Exception, e:
        raise e


def geo2addr(location='39.983424,116.322987'):
    import requests
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; BOIE9;ZHCN)',
        'Referer': 'http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-geocoding',
    }

    url = 'http://api.map.baidu.com/geocoder/v2/?ak=E4805d16520de693a3fe707cdc962045&callback=renderReverse' \
          '&location=%s&output=json&pois=1' % location
    req = requests.get(url, headers=headers)
    txt = req.content
    txt = txt.replace('renderReverse&&renderReverse(', '').replace(')', '')

    return txt


def pushMessage(messages=None, extra=None, *args, **kwargs):
    template = Template(messages)
    messages = template.render(dict(*args, **kwargs))

    push = jpush.JPush(settings.JPUSH_APPKEY, settings.JPUSH_SECRET)
    push = push.create_push()

    push.notification = jpush.notification(alert=messages, ios=messages, android=messages)
    push.options = {"time_to_live": 86400, "sendno": 12345, "apns_production": False}
    push.platform = jpush.platform("ios", "android")
    push.send()


def do_push_msgs(msgs=None, mobile=None, registration_id=None, *args, **kwargs):
    opts = jpush.JPush(settings.JPUSH_APPKEY, settings.JPUSH_SECRET)
    push = opts.create_push()

    extras = {'mobile': mobile}

    push.notification = jpush.notification(alert=msgs)

    push.options = {"time_to_live": 86400, "apns_production": True, 'extras': extras}

    push.audience = jpush.audience(jpush.registration_id(registration_id)) if registration_id else jpush.all_
    push.platform = jpush.all_

    push.send()

