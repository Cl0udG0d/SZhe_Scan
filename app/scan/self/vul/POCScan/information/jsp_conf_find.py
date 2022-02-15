#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: java配置文件文件发现
referer: unknow
author: Lucifer
description: web.xml是java框架使用的配置文件，可以获取敏感信息
'''
import sys
import requests


class jsp_conf_find_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        payload = "/WEB-INF/web.xml"
        vulnurl = self.url + payload
        try:
            req = requests.get(vulnurl, timeout=10, verify=False)
            if req.headers["Content-Type"] == "application/xml":
                return True,vulnurl,"java配置文件文件发现",payload,req.text
            else:
                return False, None, None, None, None
        except:
            return False, None, None, None, None


if __name__ == "__main__":
    testVuln = jsp_conf_find_BaseVerify(sys.argv[1])
    testVuln.run()
