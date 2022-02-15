#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: svn源码泄露扫描
referer: unknown
author: Lucifer
description: 忘记了删除.svn目录而导致的漏洞。
'''
import re
import sys
import requests


class svn_check_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payload = "/.svn/entries"
        vulnurl = self.url + payload
        try:
            req = requests.get(vulnurl, headers=headers, timeout=10, verify=False, allow_redirects=False)
            try:
                contents = str(req.text).split('\x0c')
                pattern = re.compile(r'has-props|file|dir')
                for content in contents:
                    match = len(pattern.search(content).group(0))
                    if req.status_code == 200 and match > 0:
                        return True,vulnurl,"svn源码泄露扫描",payload,req.text
                    else:
                        return False, None, None, None, None
            except:
                return False, None, None, None, None
        except:
            return False, None, None, None, None


if __name__ == "__main__":
    testVuln = svn_check_BaseVerify(sys.argv[1])
    testVuln.run()
