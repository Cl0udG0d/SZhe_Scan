#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2021/12/31 19:22
# @Author  : Cl0udG0d
# @File    : loginlog.py
# @Github: https://github.com/Cl0udG0d

from app.utils.decorators import login_required
from app.model.exts import db
from app.log import log
from flask import (
    render_template,redirect,url_for
)
from app.model.models import (
    Log
)


@log.route('/log/login/')
@log.route('/log/login/<int:page>', methods=['GET'])
# @login_required
def loginlog(page=1):
    per_page = 38
    paginate = Log.query.order_by(Log.date.desc()).paginate(page, per_page, error_out=False)
    logs = paginate.items
    return render_template('loginlog.html', paginate=paginate, logs=logs)

@log.route('/log/login/delLoginLog/<int:id>', methods=['GET'])
# @login_required
def delLoginLog(id):
    delLog=db.session.query(Log).filter_by(id=id).first()
    db.session.delete(delLog)
    db.session.commit()
    return redirect(url_for('log.loginlog'))

@log.route('/log/login/delAllLoginLog/', methods=['GET'])
# @login_required
def delAllLoginLog():
    delLogs = db.session.query(Log).all()
    [db.session.delete(delLog) for delLog in delLogs]
    db.session.commit()
    return redirect(url_for('log.loginlog'))

def test():
    print('hi')


if __name__ == '__main__':
    test()
