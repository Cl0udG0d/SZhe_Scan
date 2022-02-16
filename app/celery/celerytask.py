#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/2/16 12:23
# @Author  : Cl0udG0d
# @File    : celerytask.py
# @Github: https://github.com/Cl0udG0d
import time

from celery import Celery
from init import app
from app.model.models import Task,scanTask
from app.model.exts import db
from app.scan.scanIndex import scanConsole

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
    try:
        scanConsole(url)
    except Exception as e:
        self.update_state(state="FAILURE")
    else:
        self.update_state(state="SUCCESS")
    return

@scantask.task(bind=True)
def startScan(self,targets,key):
    self.update_state(state="PROGRESS")
    time.sleep(8)
    for url in targets:
        scantask=scanTarget.delay(url)
        temptask = scanTask(tid=scantask.task_id,
                            starttime=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
                            endtime=str("0-0-0 0:0:0"), key=str(key))
        db.session.add(temptask)
    db.session.commit()

def test():
    print('hi')


if __name__ == '__main__':
    test()
