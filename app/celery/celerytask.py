#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/2/16 12:23
# @Author  : Cl0udG0d
# @File    : celerytask.py
# @Github: https://github.com/Cl0udG0d
import os
import sys
import time

from celery import Celery, platforms
from init import app
from app.model.models import (
    Task,scanTask,PocList,pluginList
)
from app.model.exts import db
from app.scan.scanIndex import scanConsole
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)
sys.path.append(os.getcwd())
'''
celery -A app.celery.celerytask:scantask worker -c 10 --loglevel=info -P eventlet
'''
def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


scantask = make_celery(app)
platforms.C_FORCE_ROOT = True
scantask.conf.update(app.config)


def updateTaskEndTime(id):
    '''
    更新任务结束时间
    '''
    task = scanTask.query.filter_by(tid=id).first()
    task.endtime=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    db.session.commit()



def getPocAndPlugin():
    pocs = PocList.query.all()
    plugins = pluginList.query.all()
    poclist,pluginlist = list(),list()

    for poc in pocs:
        if poc.status:
            poclist.append([poc.filename, poc.position])


    for plugin in plugins:
        if plugin.status:
            pluginlist.append([plugin.filename, plugin.position])

    return poclist,pluginlist



@scantask.task(bind=True)
def scanTarget(self,url):
    # task = Task.query.filter(Task.key == key).first()
    self.update_state(state="PROGRESS")
    # print(scanTarget.request.id)

    poclist,pluginlist=getPocAndPlugin()
    try:
        scanConsole(url,poclist,self.request.id,pluginlist)
    except Exception as e:
        # print(e)
        self.update_state(state="FAILURE")
        logger.warning(e)
        pass
    else:
        updateTaskEndTime(self.request.id)



@scantask.task(bind=True)
def startScan(self,targets):
    time.sleep(3)
    for url in targets:
        scantask=scanTarget.delay(url)
        temptask = scanTask(pid=self.request.id,tid=scantask.task_id,url=url,
                                starttime=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
                                endtime=str("0-0-0 0:0:0"))
        db.session.add(temptask)
    db.session.commit()



if __name__ == '__main__':
    from app.scan.scanIndex import scanPocs
    with app.app_context():
        poclist,pluginlist=getPocAndPlugin()

        scanPocs("http://5.251.142.195:999/", poclist, "1")
        # print(poclist)
