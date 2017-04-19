# -*- coding: utf-8 -*-
"""
    :author: handsome Fu (付贞强)
    :copyright: © 2019 handsomeFu <mrfu1998@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask import Flask, jsonify

app = Flask('bbs')


@app.route('/')
def hello_world():
    return jsonify({"code": 200, "msg": "Hello Flask"})
