import requests
import core
import re
import time
from Wappalyzer import WebPage
import get_message
import ImportToRedis
import redis
from WebLogicScan import WebLogicScan
from init import app
from exts import db
from models import BugList
from init import redispool
from POCScan import selfpocscan
'''
获取输入网址基础信息:
    1,WEB指纹识别,技术识别 Finger 
    2,状态码 Status
    3,标题 Title
    4,收录扫描时间 Date
    5,响应包 response
    6,端口开放信息
    
'''


class GetBaseMessage():
    def __init__(self, url, attackurl,rep):
        print("hi!")
        self.domain = url
        self.redispool = redispool
        self.url=attackurl
        self.rep=rep

    def GetStatus(self):
        print("status")
        return str(self.rep.status_code)

    def GetTitle(self):
        print("title")
        if self.rep != None:
            return re.findall('<title>(.*?)</title>', self.rep.text)[0]
        return None

    def GetDate(self):
        print("date")
        return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    def GetResponseHeader(self):
        print("response")
        context=""
        for key, val in self.rep.headers.items():
            context += (key + ": " + val + "\r\n")
        return context

    def GetFinger(self):
        print("finger")
        return WebPage(self.url, self.rep).info()

    def PortScan(self):
        print("port")
        return get_message.PortScan(self.domain)

    def SenDir(self):
        print("sendir")
        return get_message.SenFileScan(self.domain,self.url)

    def WebLogicScan(self):
        print("weblogic")
        results=WebLogicScan.run(self.domain)
        with app.app_context():
            for result in results:
                vulnerable, bugurl, bugname, bugdetail = result
                if vulnerable:
                    bug = BugList(oldurl=self.domain, bugurl=bugurl, bugname=bugname,
                                  buggrade=redispool.hget('bugtype', bugname),
                                  payload=bugurl, bugdetail=bugdetail)
                    db.session.add(bug)
            db.session.commit()

    def AngelSwordMain(self):
        print("angel")
        selfpocscan.AngelSwordMain(self.url)




if __name__=='__main__':
    # redispool=redis.ConnectionPool(host='127.0.0.1',port=6379, decode_responses=True)
    redispool = redis.Redis(connection_pool=ImportToRedis.redisPool)
    try:
        test=GetBaseMessage("testphp.vulnweb.com",redispool)
        # test.AngelSwordMain()
        print(test.GetStatus())
        # print(test.GetTitle())
        # print(test.GetResponseHeader())
        # print(test.GetFinger())
        # print(test.PortScan())
        # print(test.SenDir())

    except Exception as e:
        print(e)
        pass

