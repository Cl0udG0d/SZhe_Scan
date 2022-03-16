#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/3/13 0:51
# @Author  : Cl0udG0d
# @File    : phpinfo敏感信息泄露.py
# @Github: https://github.com/Cl0udG0d

from pocsuite3.api import requests
from pocsuite3.api import register_poc
from pocsuite3.api import Output, POCBase, logger
import ssl


ssl._create_default_https_context = ssl._create_unverified_context

class TestPOC(POCBase):
    vulLevel = 3
    vulID = ''
    version = '1.0'
    vulDate = ''
    references = ['']
    name = 'phpinfo敏感信息泄露'
    appPowerLink = ''
    appName = 'phpinfo'
    appVersion = ''
    vulType = 'phpinfo敏感信息泄露'
    desc = '''
    '''
    samples = ['']

    def _verify(self):
        result = {}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        }
        phpinfoList=[
            '/phpinfo.php','/1.php','/test.php'
        ]

        for path in phpinfoList:
            vulurl = "{}{}".format(
                self.url.rstrip('/'), path)
            try:
                resp = requests.get(url=vulurl, headers=headers, timeout=3, verify=False)
                if "PHP Version" in resp.text and resp.status_code == 200:
                    result['VerifyInfo'] = {}
                    result['VerifyInfo']['url'] = vulurl
                    return self.parse_attack(result)
            except Exception as e:
                logger.error("connect target '{} failed!'".format(vulurl))
                pass

        return self.parse_attack(result)



    def parse_attack(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Internet nothing returned')
        return output

register_poc(TestPOC)
