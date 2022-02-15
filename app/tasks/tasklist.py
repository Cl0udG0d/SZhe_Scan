#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/1/8 13:03
# @Author  : Cl0udG0d
# @File    : tasklist.py
# @Github: https://github.com/Cl0udG0d
from app.utils.decorators import login_required
from app.model.exts import db
from app.tasks import tasks
from flask import (
    render_template,redirect,url_for
)
from app.model.models import (
    Log
)
@tasks.route('/tasks/')
@tasks.route('/tasks/<int:page>', methods=['GET'])
# @login_required
def tasklist(page=1):
    per_page = 38
    paginate = Log.query.order_by(Log.date.desc()).paginate(page, per_page, error_out=False)
    logs = paginate.items
    return render_template('tasklist.html', paginate=paginate, logs=logs)

def test():
    print('hi')


if __name__ == '__main__':
    test()
