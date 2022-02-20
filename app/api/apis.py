#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/2/20 23:02
# @Author  : Cl0udG0d
# @File    : apis.py
# @Github: https://github.com/Cl0udG0d
from flask import (
    jsonify
)
from app.api import api
from celery.result import AsyncResult
from app.celery.celerytask import scantask

@api.route('/api/gettaskstatus/<tid>', methods=['GET'])
def gettaskstatus(tid=None):
    result = AsyncResult(tid, app=scantask)
    summary = {
        "state": result.state,
    }
    return jsonify(summary), 200




def test():
    print('hi')


if __name__ == '__main__':
    test()
