#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/2/15 22:23
# @Author  : Cl0udG0d
# @File    : scanIndex.py
# @Github: https://github.com/Cl0udG0d
from app.utils.selfrequests import getRep
from app.utils.baseMsg import GetBaseMessage
from app.model.models import (
    BaseInfo
)
from app.model.exts import db
from init import app
from pocsuite3.api import init_pocsuite
from pocsuite3.api import start_pocsuite
from pocsuite3.api import get_results
import os


def scanPoc(url):
    config = {
        'url': url,
        'poc': os.path.join(os.path.dirname(os.path.dirname(__file__)), "../pocs/test.py"),
    }
    print(os.path.dirname(os.path.dirname(__file__)))
    # config字典的配置和cli命令行参数配置一模一样
    init_pocsuite(config)
    start_pocsuite()
    result = get_results().pop()
    print(result['result'])

def scanConsole(url):
    rep,target=getRep(url)
    if not rep:
        raise "error"
    basemsg=GetBaseMessage(url,target,rep)
    with app.app_context():
        basemsgdb=BaseInfo(url=url,status=basemsg.GetStatus(),title=basemsg.GetTitle(),date=basemsg.GetDate(),responseheader=basemsg.GetResponseHeader(),Server=basemsg.GetFinger())
        db.session.add(basemsgdb)
        db.session.commit()

    return

def test():
    url = "202.202.157.110"
    pattern = re.compile('^\d+\.\d+\.\d+\.\d+(:(\d+))?$')
    # 判断IP是否存在端口
    if pattern.findall(url) and ":" in url:
        infourl = url.split(":")[0]
    else:
        infourl = url
    print('hi')


if __name__ == '__main__':
    scanPoc('http://58.20.57.73:88/')
