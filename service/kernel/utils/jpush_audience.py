# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import jpush as jpush
from jpush import common
from django.conf import settings


def jpush_push(message, alias, *args, **kwargs):
    '''
    别名推送
    * @param  推送消息
    * @param  推送别名

    '''
    appkey = settings.JPUSH_APPKEY
    secret = settings.JPUSH_SECRET
    _jpush = jpush.JPush(appkey, secret)

    # the default logging level is WARNING,if you set the logging level to "DEBUG",the it will show the debug logging
    _jpush.set_logging("DEBUG")
    push = _jpush.create_push()
    push.audience = jpush.audience(
        # jpush.tag("tag1", "tag2"),
        jpush.alias(alias)
    )
    push.notification = jpush.notification(alert=message)
    push.platform = jpush.all_

    try:
        return push.send()
    except common.Unauthorized:
        raise common.Unauthorized("Unauthorized")
    except common.APIConnectionException:
        raise common.APIConnectionException("conn")
    except common.JPushFailure:
        print ("JPushFailure")
    except:
        print ("Exception")


def jpush_all(message):
    '''
    全体推送
    * @param  推送消息

    '''
    appkey = settings.JPUSH_APPKEY
    secret = settings.JPUSH_SECRET
    _jpush = jpush.JPush(appkey, secret)

    push = _jpush.create_push()

    # the default logging level is WARNING,if you set the logging level to "DEBUG",the it will show the debug logging
    _jpush.set_logging("DEBUG")
    push.audience = jpush.all_
    push.notification = jpush.notification(alert=message)
    push.platform = jpush.all_

    try:
        return push.send()
    except common.Unauthorized:
        raise common.Unauthorized("Unauthorized")
    except common.APIConnectionException:
        raise common.APIConnectionException("conn")
    except common.JPushFailure:
        print ("JPushFailure")
    except:
        print ("Exception")

