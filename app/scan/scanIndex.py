#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/2/15 22:23
# @Author  : Cl0udG0d
# @File    : scanIndex.py
# @Github: https://github.com/Cl0udG0d
import re

from app.utils.selfrequests import getRep
from app.utils.baseMsg import GetBaseMessage
from app.model.models import (
    BaseInfo,VulList
)
from app.model.exts import db
from init import app
from pocsuite3.api import init_pocsuite
from pocsuite3.api import start_pocsuite
from pocsuite3.api import get_results
import os

def saveVul(result):
    with app.app_context():
        vul=VulList(url=result['url'],pocname=result['poc_name'],pocDesc=result['poc_attrs']['pocDesc'],references=result['poc_attrs']['references'],created=result['created'])
        db.session.add(vul)
        db.session.commit()

def scanPoc(url,poc):
    config = {
        'url': url,
        'poc': os.path.join(os.path.dirname(os.path.dirname(__file__)), "../pocs/",poc),
    }
    # print(config['poc'])
    # print(os.path.dirname(os.path.dirname(__file__)))
    # config字典的配置和cli命令行参数配置一模一样
    init_pocsuite(config)
    start_pocsuite()
    result = get_results().pop()
    if result['status']=='success':
        saveVul(result)



def scanPocs(url,curr=False):

    listdir=os.path.join(os.path.dirname(os.path.dirname(__file__)),"../pocs/") if not curr else os.path.join(os.path.dirname(os.path.dirname(__file__)),"../pocs/currency/")
    for files in os.listdir(listdir):
        if os.path.splitext(files)[1] == '.py':
            scanPoc(url,files)
    return


def scanConsole(url):
    rep,target=getRep(url)
    if not rep:
        raise "error"
    basemsg=GetBaseMessage(url,target,rep)
    with app.app_context():
        basemsgdb=BaseInfo(url=url,status=basemsg.GetStatus(),title=basemsg.GetTitle(),date=basemsg.GetDate(),responseheader=basemsg.GetResponseHeader(),Server=basemsg.GetFinger())
        db.session.add(basemsgdb)
        db.session.commit()
    scanPocs(target)
    results=spiderWebSite(target)
    scanPocs(results)
    return

def test():
    url = "https://www.cnblogs.com//css/blog-common.min.css?v=oyR94yG9E65eGarh4GfroLpfiKQIbUAj9f7aXieEDQQ"
    filter_pattern = re.compile(
        '/\w+.*\.(css|png|gif|jpg|jpeg|swf|tiff|pdf|ico|flv|mp4|mp3|avi|mpg|gz|mpeg|iso|dat|rar|mov|exe|tar|zip|bin|bz2|xsl|'
        'doc|docx|ppt|pptx|xls|xlsx|csv|map|ttf|tif|woff|woff2|cab|apk'
        '|bmp|svg|exif|xml|rss|webp|js|html)\?')
    # 判断IP是否存在端口
    if filter_pattern.findall(url):
        print(filter_pattern.findall(url))
    else:
        infourl = url
    print('hi')


if __name__ == '__main__':
    # scanPoc('http://58.20.57.73:88/',"test")
    test()