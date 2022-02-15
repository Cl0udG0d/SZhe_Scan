#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: 正方教务系统default3.aspx爆破页面
referer: http://www.wooyun.org/bugs/WooYun-2013-21692
author: Lucifer
description: 文件default3.aspx页面可爆破。
'''
import sys
import requests
import warnings
from termcolor import cprint

class zfsoft_default3_bruteforce_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        try:
            req = requests.get(self.url, headers=headers, timeout=6, verify=False, allow_redirects=True)
        except:
            pass
        tmpurl = str(req.url)
        tmpurl = tmpurl.lower()
        if r"default2.aspx" in tmpurl or r"default.aspx" in tmpurl:
            vulnurl = tmpurl.replace("default2.aspx","").replace("default.aspx", "")
        else:
            vulnurl = tmpurl
        vulnurl = vulnurl + "default3.aspx"
        try:
            req = requests.get(vulnurl, headers=headers, timeout=10, verify=False)
            if r"__VIEWSTATEGENERATOR" in req.text and r"CheckCode.aspx" not in req.text and req.status_code ==200:
                cprint("[+]存在正方教务系统default3.aspx爆破页面...(敏感信息)\tpayload: "+vulnurl, "green")
                return True, vulnurl, "正方教务系统default3.aspx爆破页面", vulnurl, req.text
            else:
                cprint("[-]不存在zfsoft_default3_bruteforce漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = zfsoft_default3_bruteforce_BaseVerify(sys.argv[1])
    testVuln.run()
