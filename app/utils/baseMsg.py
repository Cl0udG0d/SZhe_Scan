#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/2/16 16:45
# @Author  : Cl0udG0d
# @File    : baseMsg.py
# @Github: https://github.com/Cl0udG0d
import re
import logging
import time
from app.utils.Wappalyzer import WebPage


logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.DEBUG)


class GetBaseMessage():
    def __init__(self, url, attackurl,rep):
        self.domain = url
        self.url=attackurl
        self.rep=rep

    def GetStatus(self):
        logging.info("正在获取网页状态码")
        try:
            return str(self.rep.status_code)
        except Exception as e:
            logging.warning(e)
            pass

    def GetTitle(self):
        logging.info("正在获取网页标题!")
        try:
            title=re.findall('<title>(.*?)</title>', self.rep.text)[0]
            return title
        except Exception as e:
            logging.warning(e)
            pass

    def GetDate(self):
        logging.info("正在获取系统当前时间!")
        return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    def GetResponseHeader(self):
        logging.info("正在获取网页响应头!")
        context = ""
        try:
            for key, val in self.rep.headers.items():
                context += (key + ": " + val + "\r\n")
            return context
        except Exception as e:
            logging.warning(e)
            pass

    def GetFinger(self):
        logging.info("指纹识别")
        try:
            finger=WebPage(self.url, self.rep).info()
            return finger
        except Exception as e:
            logging.warning(e)
            pass


def test():
    print('hi')


if __name__ == '__main__':
    test()
