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
    Log,Task,scanTask,BaseInfo,VulList
)
from app.celery.celerytask import startScan
from app.utils.filter import check2filter
from app.model.exts import db
import time
from sqlalchemy import func


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
    task = startScan.delay(newTarget)
    temptask = Task(tid=task.task_id, name=targetname,
                    starttime=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
                    endtime=str("0-0-0 0:0:0"))
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

@tasks.route('/tasks/deltasks/<tid>', methods=['GET'])
def deltasks(tid=None):
    tasks= Task.query.filter(Task.tid == tid).first()
    scantasks=scanTask.query.filter(scanTask.pid == tasks.tid)
    [db.session.delete(task) for task in scantasks]
    db.session.delete(tasks)
    db.session.commit()
    flash("删除成功")
    return redirect(url_for('tasks.tasklist'))


@tasks.route('/tasks/deltask/<id>/<tid>', methods=['GET'])
def deltask(id=1,tid=None):
    tasks = scanTask.query.filter(scanTask.tid == tid).first()
    db.session.delete(tasks)
    db.session.commit()
    flash("删除成功")
    return redirect(url_for('tasks.seetask',id=id))

@tasks.route('/tasks/seetask/<id>', methods=['GET'])
def seetask(id=None):
    tasks= Task.query.filter(Task.id == id).first()
    scantasks=scanTask.query.filter(scanTask.pid == tasks.tid).all()
    return render_template('scantask.html',tasks=tasks,scantasks=scantasks)



@tasks.route('/tasks/scanreport/<id>/<tid>', methods=['GET'])
def scanreport(id=None,tid=None):
    task= Task.query.filter(Task.id == id).first()
    scantask=scanTask.query.filter(scanTask.tid == tid).first()
    info=BaseInfo.query.filter(BaseInfo.tid == tid).first()
    vuls=VulList.query.filter(VulList.tid == tid).first()
    return render_template('scanreport.html',task=task,scantask=scantask,info=info,vuls=vuls)



def returnStatus(tid):
    return



@tasks.route('/test', methods=['GET'])
def test():
    return render_template('scanreport.html')



if __name__ == '__main__':
    test()
