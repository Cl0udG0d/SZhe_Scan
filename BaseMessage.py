import requests
import core
import re
import time
import redis
from Wappalyzer import WebPage
import get_message
# import ImportToRedis
import json
from models import BaseInfo
<<<<<<< HEAD

=======
import redis
>>>>>>> 2218520bbb6eb632e91f61ea9153a2848062d5e8
'''
获取输入网址基础信息:
    1,WEB指纹识别,技术识别 Finger 
    2,状态码 Status
    3,标题 Title
    4,收录扫描时间 Date
    5,响应包 response
    6,端口开放信息
    
'''
options = {1: 'self.GetStatus', 2: 'self.GetTitle', 3: 'self.GetDate', 4: 'self.GetResponseHeader', 5: 'self.GetFinger',
           6: 'self.PortScan'}


class GetBaseMessage():
    def __init__(self, url, redispool):
        self.domain = url
        self.redispool = redispool
        self.list = ['self.GetStatus','self.GetTitle', 'self.GetDate', 'self.GetResponseHeader', 'self.GetFinger',
           'self.PortScan', 'self.SenDir']
        try:
            if not (url.startswith("http://") or url.startswith("https://")):
                self.url = "http://" + url
            else:
                self.url = url
            self.rep = requests.get(self.url, headers=core.GetHeaders(), timeout=3, verify=False)
        except:
            self.rep = None
            pass
        if self.rep == None:
            try:
                self.url = "https://" + url
                self.rep = requests.get(self.url, headers=core.GetHeaders(), timeout=3, verify=False)
            except:
                pass
<<<<<<< HEAD
        # for i in range(1, 8):
            # if i in options:
            #     tar = options[i]
            # else:
            #     tar = 'self.SenDir'
            # tar = self.tar
            # t = threading.Thread(target=self.list[i-1])
            # t.start()

        self.status = self.GetStatus()
        self.title = self.GetTitle()
        self.date = self.GetDate()
        self.responseHeader = self.GetResponseHeader()
        self.finger = self.GetFinger()
        self.portScan = self.PortScan()
        self.senDir = self.SenDir()
=======
        print(self.SenDir())
>>>>>>> 2218520bbb6eb632e91f61ea9153a2848062d5e8

    def GetStatus(self):
        return str(self.rep.status_code)

    def GetTitle(self):
        if self.rep != None:
            return re.findall('<title>(.*?)</title>', self.rep.text)[0]
        return None

    def GetDate(self):
        return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    def GetResponseHeader(self):
        return str(self.rep.headers)

    def GetFinger(self):
        return WebPage(self.url, self.rep).info()

    def PortScan(self):
        return get_message.PortScan(self.domain)

    def SenDir(self):
        return get_message.SenFileScan(self.domain, self.redispool)


<<<<<<< HEAD
if __name__ == '__main__':
    redispool=redis.Redis(connection_pool=ImportToRedis.redisPool)
    test = GetBaseMessage("www.baidu.com", redispool)
    print("end!")
=======
if __name__=='__main__':
    # redispool=redis.ConnectionPool(host='127.0.0.1',port=6379, decode_responses=True)
    # test=GetBaseMessage("www.baidu.com",redispool)
    print("end!")
>>>>>>> 2218520bbb6eb632e91f61ea9153a2848062d5e8
