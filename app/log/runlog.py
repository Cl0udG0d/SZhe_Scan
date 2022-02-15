#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/1/5 16:04
# @Author  : Cl0udG0d
# @File    : runlog.py
# @Github: https://github.com/Cl0udG0d
from app.utils.decorators import login_required
from app.log import log
from flask import (
    render_template
)
from app.model.models import (
    Log
)


# 日志每页显示38条
@log.route('/log/run/')
@log.route('/log/run/<int:page>', methods=['GET'])
@login_required
def runlog(page=1):
    per_page = 38
    paginate = Log.query.order_by(Log.date.desc()).paginate(page, per_page, error_out=False)
    logs = paginate.items
    return render_template('loginlog.html', paginate=paginate, logs=logs)
def test():
    print('hi')


if __name__ == '__main__':
    test()
