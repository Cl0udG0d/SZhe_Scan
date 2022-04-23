#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/1/8 13:03
# @Author  : Cl0udG0d
# @File    : tasklist.py
# @Github: https://github.com/Cl0udG0d
import logging
import os

from app.tasks import tasks
from flask import (
    render_template,redirect,url_for,request,flash,make_response
)
from app.model.models import (
    Log,Task,scanTask,BaseInfo,VulList,ExtList
)
from app.celery.celerytask import startScan
from app.utils.filter import check2filter
from app.model.exts import db
import time
from app.utils.decorators import login_required
from init import app
import mimetypes


@tasks.route('/tasks/')
@tasks.route('/tasks/<int:page>', methods=['GET'])
@login_required
def tasklist(page=1,msg=None):
    paginate = Task.query.order_by(Task.id.desc()).paginate(page=page, per_page=10, error_out=False)
    tasks = paginate.items
    return render_template('tasklist.html', pagination=paginate,tasks=tasks)



@tasks.route('/tasks/addtask', methods=['POST'])
@login_required
def addtask():
    targets=request.form.get('targets')
    targetname=request.form.get('targetname')
    newTarget,length=check2filter(targets)
    with app.app_context():
        task = startScan.delay(newTarget)
        temptask = Task(tid=task.task_id, name=targetname,
                        starttime=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
                        endtime=str("0-0-0 0:0:0"))
        db.session.add(temptask)
        db.session.commit()
    flash("任务名称:{} 扫描数量:{} ".format(targetname,length))
    return redirect(url_for('tasks.tasklist'))



@tasks.route('/tasks/deltasks/<tid>', methods=['GET'])
@login_required
def deltasks(tid=None):
    with app.app_context():
        tasks= Task.query.filter(Task.tid == tid).first()
        scantasks=scanTask.query.filter(scanTask.pid == tasks.tid)
        [db.session.delete(task) for task in scantasks]
        db.session.delete(tasks)
        db.session.commit()
        flash("删除成功")
    return redirect(url_for('tasks.tasklist'))





@tasks.route('/tasks/deltask/<id>/<tid>', methods=['GET'])
@login_required
def deltask(id=1,tid=None):
    with app.app_context():
        tasks = scanTask.query.filter(scanTask.tid == tid).first()
        db.session.delete(tasks)
        db.session.commit()
    flash("删除成功")
    return redirect(url_for('tasks.seetask',id=id))




@tasks.route('/tasks/delAllTask', methods=['GET'])
@login_required
def delAllTask():
    with app.app_context():
        tasks = Task.query.all()
        [db.session.delete(task) for task in tasks]


        scantasks = scanTask.query.all()
        [db.session.delete(task) for task in scantasks]

        db.session.commit()
    flash("删除成功")
    return redirect(url_for('tasks.tasklist'))




@tasks.route('/tasks/seetask/<id>', methods=['GET'])
@tasks.route('/tasks/seetask/<id>/<int:page>', methods=['GET'])
@login_required
def seetask(page=1,id=1):
    tasks= Task.query.filter(Task.id == id).first()
    paginate=scanTask.query.filter(scanTask.pid == tasks.tid).order_by(scanTask.id.desc()).paginate(page=page, per_page=10, error_out=False)
    scantasks=paginate.items
    return render_template('scantask.html',pagination=paginate,tasks=tasks,scantasks=scantasks)





@tasks.route('/tasks/scanreport/<id>/<tid>', methods=['GET'])
@login_required
def scanreport(id=None,tid=None):
    task= Task.query.filter(Task.id == id).first()
    scantask=scanTask.query.filter(scanTask.tid == tid).first()
    info=BaseInfo.query.filter(BaseInfo.tid == tid).first()
    vuls=VulList.query.filter(VulList.tid == tid).all()
    exts=ExtList.query.filter(ExtList.tid == tid).all()
    if not info:
        flash("任务正在执行或执行出错，无法查看")
        return redirect(url_for('tasks.seetask', id=id))
    return render_template('scanreport.html',task=task,scantask=scantask,info=info,vuls=vuls,exts=exts)


@tasks.route('/tasks/outputreport/<id>/<tid>', methods=['GET'])
@login_required
def outputReport(id=None,tid=None):
    task= Task.query.filter(Task.id == id).first()
    scantask=scanTask.query.filter(scanTask.tid == tid).first()
    info=BaseInfo.query.filter(BaseInfo.tid == tid).first()
    vuls=VulList.query.filter(VulList.tid == tid).all()
    exts=ExtList.query.filter(ExtList.tid == tid).all()
    if not info:
        flash("任务正在执行或执行出错，无法查看")
        return redirect(url_for('tasks.seetask', id=id))
    # directory = os.getcwd()  # 假设在当前目录
    filename="SHZE-{}-{}.html".format(id,tid)
    # filecontent=tasks.send_static_file('outputReport.html',task=task,scantask=scantask,info=info,vuls=vuls,exts=exts)
    filecontent=render_template('outputReport.html',task=task,scantask=scantask,info=info,vuls=vuls,exts=exts)
    # pathname = os.path.join(os.path.join(os.getcwd(), "../../temp"),filename)
    # f = open(pathname, "rb")
    # response = Response(f.readlines())
    response = make_response(filecontent)
    mime_type = mimetypes.guess_type(filename)[0]
    response.headers['Content-Type'] = mime_type
    response.headers['Content-Disposition'] = 'attachment; filename={}'.format(filename.encode().decode('latin-1'))
    return response
    # return render_template('outputReport.html',task=task,scantask=scantask,info=info,vuls=vuls,exts=exts)


ALLOWED_EXTENSIONS = set(['txt'])
from werkzeug.utils import secure_filename

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



@tasks.route('/tasks/uploadTarget/', methods=['POST'])
@login_required
def uploadTarget():
    file = request.files.get("file")
    if file and allowed_file(file.filename):
        targets=file.read().decode('ascii')
        targetname = secure_filename(file.filename).split('.')[0] if '.' in secure_filename(file.filename) else secure_filename(file.filename)
        newTarget, length = check2filter(targets)
        with app.app_context():
            task = startScan.delay(newTarget)
            temptask = Task(tid=task.task_id, name=targetname,
                            starttime=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
                            endtime=str("0-0-0 0:0:0"))
            db.session.add(temptask)
            db.session.commit()
        flash("任务名称:{} 扫描数量:{} ".format(targetname, length))
    else:
        flash('上传失败')
    return redirect(url_for('tasks.tasklist'))



if __name__ == '__main__':
    print(os.path.join(os.getcwd(), "../../temp"))
