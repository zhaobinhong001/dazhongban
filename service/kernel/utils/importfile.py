# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import pandas as pd
import numpy as np

from service.signature.models import BANKID


def impotrbank():
    '''
    导出h5文件

    '''
    # 读取excel文件数据
    df = pd.read_excel('./resources/demo.xls', encoding='utf-8')
    # 设置列名
    df.columns = [u'name', 'bank', 'card', 'type']
    # 从第四条记录开始取值
    df = df.iloc[3:]
    # 清除空信息

    # 遍历需要的银行卡
    alist = [x[1] for x in BANKID]
    # 遍历excel文档获取全部银行信息
    for index, x in df.iterrows():
        # 截取多余的字符
        x['name'] = x['name'][:-11]
        # 过滤空信息
        # 过滤不需要银行
        if x['name'] not in alist:
            df = df.drop(index, axis=0)
        # for xx in alist:
        #     if xx in x['name']:
        #         # 加个标记
        #         df['sign'] = x['name']
        #         # 加正常名
        #         df['realbank'] = xx

    # # 导出高性能文件格式 hdf5
    df.to_hdf('./resources/bankcard.h5', 'df')
