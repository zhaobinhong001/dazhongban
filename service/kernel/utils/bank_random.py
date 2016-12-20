# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import datetime
import random
import time


def bankcard():
    '''
    模拟银行卡号

    '''
    nowTime = int(time.mktime(datetime.datetime.now().timetuple()))  # 生成当前时间
    randomNum = str(random.randint(0, 999)).zfill(3)
    bankID = '845393'
    return bankID + str(nowTime) + randomNum
