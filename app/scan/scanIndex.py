#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/2/15 22:23
# @Author  : Cl0udG0d
# @File    : scanIndex.py
# @Github: https://github.com/Cl0udG0d
import logging
import re
import time

from app.utils.selfrequests import getRep
from app.utils.baseMsg import GetBaseMessage
from app.utils.szheException import (
    reqBadExceptin
)
from app.model.models import (
    BaseInfo, VulList, ExtList
)
from app.model.exts import db
from app.utils.spider import spider

from init import app
from pocsuite3.api import init_pocsuite
from pocsuite3.api import start_pocsuite
from pocsuite3.api import get_results
import os
import json
from app.utils.beforeScan import getPluginDepends



def saveVul(result,tid,poc):
    with app.app_context():
        vul=VulList(url=result['url'],tid=tid,pocname=poc,result=json.dumps(result['result']['VerifyInfo']),created=result['created'])
        db.session.add(vul)
        db.session.commit()



def saveExts(result,tid,pluginname):
    with app.app_context():
        extMsg=ExtList(pluginname=pluginname,tid=tid,result=result,created=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

        db.session.add(extMsg)
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



def scanPocs(url,poclist,tid,position=False):
    currdir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "../pocs/")
    for poc in poclist:
        if poc[1]==position:
            try:
                scanPoc(url,currdir,poc[0],tid)
            except Exception as e:
                logging.info(e)
                pass



def scanPlugins(url,pluginlist,tid,position=False):

    # currdir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "../plugins/")
    for plugin in pluginlist:
        if plugin[1]==position:
            # try:
            scanPlugin(url,plugin[0],tid)
            # except Exception as e:
            #     logging.info(e)
            #     pass



def scanPlugin(url,plugin,tid):
    # config = {
    #     'url': url,
    #     'plugin': os.path.join(currdir, plugin + '.py'),
    # }
    # print(config['poc'])
    # print(os.path.dirname(os.path.dirname(__file__)))
    # config字典的配置和cli命令行参数配置一模一样
    # plugin = __import__("plugins." + plugin, fromlist=[plugin])
    tempPlugin = __import__("plugins.{}".format(plugin), fromlist=[plugin])
    # Errors may be occured. Handle it yourself.
    result=tempPlugin.run(url)
    saveExts(result, tid, plugin)
    # if result['status'] == 'success':
    #     logging.info("success")
        # saveVul(result, tid, poc)





def scanConsole(url,poclist,tid,pluginlist):
    rep,target=getRep(url)
    if not rep:
        raise reqBadExceptin(url)
    basemsg=GetBaseMessage(url,target,rep)
    with app.app_context():
        basemsgdb=BaseInfo(url=url,tid=tid,status=basemsg.GetStatus(),title=basemsg.GetTitle(),date=basemsg.GetDate(),responseheader=basemsg.GetResponseHeader(),Server=basemsg.GetFinger())
        db.session.add(basemsgdb)
        db.session.commit()

    # 预处理
    getPluginDepends()

    time.sleep(5)
    # 前置扫描
    scanPocs(target,poclist,tid)
    scanPlugins(target,pluginlist,tid)

    results=spider(target)

    # 后置扫描
    for tempurl in results:
        scanPocs(tempurl, poclist, tid, position=True)
        scanPlugins(tempurl, pluginlist, tid, position=True)

    logging.info("{} ScanEnd".format(url))



def test():
    print('hi')


if __name__ == '__main__':
    scanPoc("http://127.0.0.1","C:\\Users\\Cl0udG0d\\Desktop\\SZhe_Scan\\pocs","phpMyAdmin 弱密码漏洞","1")