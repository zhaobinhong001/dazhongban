# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import pandas as pd

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
    # 增加一列数据
    df['oldcard'] = '*'
    df['bankID'] = '*'
    # 遍历需要的银行卡
    alist = [x[1] for x in BANKID]

    banks = {}
    for bank in BANKID:
        banks[bank[1]] = bank[0]

    # 遍历excel文档获取全部银行信息
    for index, x in df.iterrows():
        # 截取多余的字符
        x['name'] = x['name'][:-11]
        # for y in banks:
        #     if x['name'] == y[1]:
        #         df['bankid'] = y[0]
        if x['name'] not in alist:
            df = df.drop(index, axis=0)
    # 遍历赋值
    for index, x in df.iterrows():
        # 截取多余的字符
        x['name'] = x['name'][:-11]
        x['bankID'] = banks[x['name']]
        # 保留原始银行卡号
        x['oldcard'] = x['card']
        # 清洗数据
        x['card'] = x['card'].replace('x', u'')
        x['card'] = x['card'].replace('X', u'')
        #
        # x['bankid'] = banks[u"'" + x['name'] + "'"]

    # 导出高性能文件格式 hdf5
    df.to_hdf('./resources/bankcard.h5', 'df')
    # 导出excel格式 文件
    # df.to_excel('./resources/bankcard.xlsx')
