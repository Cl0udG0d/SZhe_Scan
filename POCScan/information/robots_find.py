#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: robots文件发现
referer: unknow
author: Lucifer
description: robots.txt是爬虫标准文件，可从文件里找到屏蔽了哪些爬虫搜索的目录
'''
import sys
import requests
import warnings
from termcolor import cprint

class robots_find_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        payload = "/robots.txt"
        vulnurl = self.url + payload
        try:
            req = requests.get(vulnurl, timeout=10, verify=False)

            if "Disallow" in req.text:
                return True,vulnurl,"robots文件发现",payload,req.text
            else:
                return False, None, None, None, None
        except:
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = robots_find_BaseVerify(sys.argv[1])
    testVuln.run()
