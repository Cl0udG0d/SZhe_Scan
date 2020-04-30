import requests
import core
import re
import time
from Wappalyzer import WebPage
import get_message
import redis
import json

'''
获取输入网址基础信息:
    1,WEB指纹识别,技术识别 Finger 
    2,状态码 Status
    3,标题 Title
    4,收录扫描时间 Date
    5,响应包 response
    6,端口开放信息
    
'''
class GetBaseMessage:
    def __init__(self,url,redispool):
        self.domain=url
        self.redispool=redispool
        self.RedisConnect()
        try:
            if not (url.startswith("http://") or url.startswith("https://")):
                self.url = "http://" + url
            else:
                self.url = url
            self.rep = requests.get(self.url, headers=core.GetHeaders(), timeout=3, verify=False)
        except:
            pass
        if self.rep==None:
            try:
                self.url="https://"+url
                self.rep = requests.get(self.url, headers=core.GetHeaders(), timeout=3, verify=False)
            except:
                pass
        self.redis.hmset(self.domain,{'WebFinger':json.dumps(self.GetFinger()),'WebStatus':self.GetStatus(),'WebTitle':self.GetTitle(),'Date':self.GetDate(),'ResponseHeader':json.dumps(dict(self.GetResponseHeader())),'PortMessage':self.PortScan(),'SenMessage':self.SenMessage(),'SenDir':self.SenDir()})
    def RedisConnect(self):
        self.redis=redis.Redis(connection_pool=self.redispool)

    def GetStatus(self):
        return self.rep.status_code

    def GetTitle(self):
        if self.rep!=None:
            return re.findall('<title>(.*?)</title>', self.rep.text)[0]
        return None

    def GetDate(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def GetResponseHeader(self):
        return self.rep.headers

    def GetFinger(self):
        return WebPage(self.url,self.rep).info()

    def PortScan(self):
        return get_message.PortScan(self.domain)

    def SenMessage(self):
        return get_message.InforLeakage(self.domain)

    def SenDir(self):
        return get_message.SenFileScan(self.domain)


if __name__=='__main__':
    redispool=redis.ConnectionPool(host='127.0.0.1',port=6379, decode_responses=True)
    test=GetBaseMessage("www.baidu.com",redispool)
    print("end!")
    # print(test.GetDate())
    # print(test.GetResponse())
    # print(test.GetTitle())
    # print(test.GetStatus())
    # print(test.GetFinger())
    # print(test.PortScan())