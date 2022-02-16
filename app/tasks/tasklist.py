#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/1/8 13:03
# @Author  : Cl0udG0d
# @File    : tasklist.py
# @Github: https://github.com/Cl0udG0d
import random
from app.tasks import tasks
from flask import (
    render_template,redirect,url_for,request,flash
)
from app.model.models import (
    Log,Task
)
from app.celery.celerytask import startScan
from app.utils.filter import check2filter
from app.model.exts import db
import time

@tasks.route('/tasks/')
@tasks.route('/tasks/<int:page>', methods=['GET'])
# @login_required
def tasklist(page=1,msg=None):
    per_page = 38
    paginate = Task.query.order_by(Task.id.desc()).paginate(page, per_page, error_out=False)
    tasks = paginate.items
    return render_template('tasklist.html', paginate=paginate, tasks=tasks)

@tasks.route('/tasks/addtask', methods=['POST'])
def addtask():
    targets=request.form.get('targets')
    targetname=request.form.get('targetname')
    newTarget,length=check2filter(targets)
    key=random.randint(0,10000000)
    # print(key)
    task = startScan.delay(newTarget,key)
    temptask = Task(tid=task.task_id, name=targetname,
                    starttime=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
                    endtime=str("0-0-0 0:0:0"), key=key)
    db.session.add(temptask)
    db.session.commit()
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

def returnStatus(tid):
    return

def test():
    print('hi')

if __name__ == '__main__':
    test()
