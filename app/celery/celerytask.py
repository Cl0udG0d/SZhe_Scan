#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/2/16 12:23
# @Author  : Cl0udG0d
# @File    : celerytask.py
# @Github: https://github.com/Cl0udG0d
import time

from celery import Celery
from init import app
from app.model.models import (
    Task,scanTask,PocList
)
from app.model.exts import db
from app.scan.scanIndex import scanConsole
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

'''
celery -A app.celery.celerytask:scantask worker -c 10 --loglevel=info -P eventlet
'''
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

scantask = make_celery(app)
scantask.conf.update(app.config)

@scantask.task(bind=True)
def scanTarget(self,url):
    # task = Task.query.filter(Task.key == key).first()
    self.update_state(state="PROGRESS")
    # print(scanTarget.request.id)
    pocs=PocList.query.all()
    poclist=list()
    for poc in pocs:
        if poc.status:
            poclist.append(poc.filename)
    try:
        scanConsole(url,poclist,self.request.id)
    except Exception as e:
        print(e)
        self.update_state(state="FAILURE")
    else:
        self.update_state(state="SUCCESS")
    return

@scantask.task(bind=True)
def startScan(self,targets):
    self.update_state(state="PROGRESS")
    time.sleep(3)
    for url in targets:
        scantask=scanTarget.delay(url)
        temptask = scanTask(pid=self.request.id,tid=scantask.task_id,url=url,
                            starttime=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
                            endtime=str("0-0-0 0:0:0"))
        db.session.add(temptask)
    db.session.commit()

@scantask.task(bind=True)
def test(self):
    logger.info(self.request.id)


if __name__ == '__main__':
    test.delay()
