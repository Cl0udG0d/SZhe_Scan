#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/2/15 22:23
# @Author  : Cl0udG0d
# @File    : scanIndex.py
# @Github: https://github.com/Cl0udG0d
import logging
import re

from app.utils.selfrequests import getRep
from app.utils.baseMsg import GetBaseMessage
from app.model.models import (
    BaseInfo,VulList
)
from app.model.exts import db
from app.utils.spider import spider

from init import app
from pocsuite3.api import init_pocsuite
from pocsuite3.api import start_pocsuite
from pocsuite3.api import get_results
import os

def saveVul(result,tid,poc):
    with app.app_context():
        vul=VulList(url=result['url'],tid=tid,pocname=poc,references=result['poc_attrs']['references'],created=result['created'])
        db.session.add(vul)
        db.session.commit()

def scanPoc(url,currdir,poc,tid):
    config = {
        'url': url,
        'poc': os.path.join(currdir,poc+'.py'),
    }
    # print(config['poc'])
    # print(os.path.dirname(os.path.dirname(__file__)))
    # config字典的配置和cli命令行参数配置一模一样
    init_pocsuite(config)
    start_pocsuite()
    result = get_results().pop()
    if result['status']=='success':
        saveVul(result,tid,poc)



def scanPocs(url,poc,tid,curr=False):
    currdir=os.path.join(os.path.dirname(os.path.dirname(__file__)),"../pocs/") if not curr else os.path.join(os.path.dirname(os.path.dirname(__file__)),"../pocs/currency/")
    scanPoc(url,currdir,poc,tid)


def scanConsole(url,poclist,tid):
    rep,target=getRep(url)
    if not rep:
        raise
    basemsg=GetBaseMessage(url,target,rep)
    with app.app_context():
        basemsgdb=BaseInfo(url=url,tid=tid,status=basemsg.GetStatus(),title=basemsg.GetTitle(),date=basemsg.GetDate(),responseheader=basemsg.GetResponseHeader(),Server=basemsg.GetFinger())
        db.session.add(basemsgdb)
        db.session.commit()
    try:
        for poc in poclist:
            scanPocs(target,poc,tid)
    except Exception as e:
        print(e)

    results=spider(target)
    logging.info("end")

    # scanPocs(results,curr=True)
    # return

def test():

    print('hi')


if __name__ == '__main__':
    # scanPoc('http://58.20.57.73:88/',"test")
    test()