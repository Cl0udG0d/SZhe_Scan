#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
'''
 ____       _     _     _ _   __  __           _
|  _ \ __ _| |__ | |__ (_) |_|  \/  | __ _ ___| | __
| |_) / _` | '_ \| '_ \| | __| |\/| |/ _` / __| |/ /
|  _ < (_| | |_) | |_) | | |_| |  | | (_| \__ \   <
|_| \_\__,_|_.__/|_.__/|_|\__|_|  |_|\__,_|___/_|\_\

'''
import logging
import sys
import requests


VUL=['CVE-2018-2894']
headers = {'user-agent': 'ceshi/0.0.1'}

def islive(ur,port):
    url='http://' + str(ur)+':'+str(port)+'/ws_utc/resources/setting/options/general'
    r = requests.get(url, headers=headers)
    return r.status_code,r.text

def run(url,port):
    port=int(port)
    status,text=islive(url,port)
    if status!=404:
        u='http://' + str(url)+':'+str(port)+'/ws_utc/resources/setting/options/general'
        return True,u,"weblogic has a JAVA deserialization vulnerability:CVE-2018-2894",text
    return False,None

if __name__=="__main__":
    url = sys.argv[1]
    port = int(sys.argv[2])
    run(url,port)
