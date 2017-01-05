# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pandas import json
from flask import Flask, jsonify
from flask import render_template
from flask import request
import pandas as pd

app = Flask(__name__)


@app.route('/bank', methods=['GET', 'POST'])
@app.route('/bank/<num>', methods=['GET', 'POST'])
def bankcard(num=None):
    # 验证银行卡号
    if request.method == "POST":
        result = {}
        df = pd.read_hdf('./resources/bankcard.h5')

        for x in [8, 6, 5]:
            vv = df.loc[df['card'] == request.form['card'][:x]]
            if len(vv):
                vv = vv.iloc[0]
                del vv['card']
                del vv['oldcard']
                result.update(vv)
                # return json.dumps(result)
                return jsonify({'result': result})
        return "未找到该类型卡信息,请确认卡号书写正确"
    else:
        result = {}
        df = pd.read_hdf('./resources/bankcard.h5')

        for x in [8, 6, 5]:
            vv = df.loc[df['card'] == num[:x]]
            if len(vv):
                vv = vv.iloc[0]
                del vv['card']
                del vv['oldcard']
                result.update(vv)
                # return json.dumps(result)
                return jsonify({'result': result})

        return "未找到该类型卡信息,请确认卡号书写正确"


@app.route('/')
def hello_world():
    return render_template('bankcard.html')


if __name__ == '__main__':
    app.run(port=000, debug=True)
