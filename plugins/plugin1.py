#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/3/16 16:56
# @Author  : Cl0udG0d
# @File    : plugin1.py
# @Github: https://github.com/Cl0udG0d
import requests
import re

def run(url):
    result = {
        'status': 'fail'
    }
    vul_url = '%s/veribaze/angelo.mdb' % url
    response = requests.get(vul_url).text

    if re.search('Standard Jet DB', response):
        result['VerifyInfo'] = {}
        result['VerifyInfo']['URL'] = url
        result['VerifyInfo']['context'] = response
        result['status'] = 'success'
    return result


def test():
    print('hi')


if __name__ == '__main__':
    test()
