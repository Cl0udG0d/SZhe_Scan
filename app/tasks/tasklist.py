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
    render_template,redirect,url_for,request,flash
)
from app.model.models import (
    Log
)
from app.scan.scanIndex import startScan
from app.utils.filter import check2filter
@tasks.route('/tasks/')
@tasks.route('/tasks/<int:page>', methods=['GET'])
# @login_required
def tasklist(page=1,msg=None):
    per_page = 38
    paginate = Log.query.order_by(Log.date.desc()).paginate(page, per_page, error_out=False)
    logs = paginate.items
    return render_template('tasklist.html', paginate=paginate, logs=logs)

@tasks.route('/tasks/addtask', methods=['POST'])
def addtask():
    targets=request.form.get('targets')
    targetname=request.form.get('targetname')
    newTarget,length=check2filter(targets)
    task = startScan.delay(targetname, newTarget)
    flash("任务名称:{} 扫描数量:{} ".format(targetname,length))
    return redirect(url_for('tasks.tasklist'))

@tasks.route('/tasks/stoptask', methods=['POST'])
def stoptask():
    targets=request.form.get('targets')
    targetname=request.form.get('targetname')
    print(targets)
    return redirect(url_for('tasks.tasklist'))

@tasks.route('/tasks/deltask', methods=['POST'])
def deltask():
    targets=request.form.get('targets')
    targetname=request.form.get('targetname')
    print(targets)
    return redirect(url_for('tasks.tasklist'))

@tasks.route('/tasks/seetask', methods=['POST'])
def seetask():
    targets=request.form.get('targets')
    targetname=request.form.get('targetname')
    print(targets)
    return redirect(url_for('tasks.tasklist'))

def test():
    print('hi')

if __name__ == '__main__':
    test()
