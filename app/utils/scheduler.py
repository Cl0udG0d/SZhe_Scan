#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/2/21 14:36
# @Author  : Cl0udG0d
# @File    : scheduler.py
# @Github: https://github.com/Cl0udG0d
import datetime
import logging
import time

from flask_apscheduler import APScheduler

from app.model.models import (
    scanTask,Task
)
from init import app
from celery.result import AsyncResult
from app.celery.celerytask import scantask
from app.model.models import (
    db
)


aps = APScheduler()



def updateTaskStatus():
    with app.app_context():
        try:
            scantasks = scanTask.query.all()
            tasks=Task.query.all()
            for task in scantasks:
                result = AsyncResult(task.tid, app=scantask)
                task.status=result.state

            for task in tasks:
                result = AsyncResult(task.tid, app=scantask)
                task.status = result.state
                if result.state=='SUCCESS' and task.endtime == str("0-0-0 0:0:0"):
                    task.endtime=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


        except Exception as e:
            logging.warning(e)
            pass
        finally:
            db.session.commit()



def task(a, b):
    print(str(datetime.datetime.now()) + ' execute task ' + '{}+{}={}'.format(a, b, a + b))



def schedulerStart():
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()



def test():
    print('hi')



if __name__ == '__main__':
    test()
