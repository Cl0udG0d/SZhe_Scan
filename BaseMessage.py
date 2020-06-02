import requests
import core
import re
import time
from Wappalyzer import WebPage
import get_message
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
        self.domain = url
        self.redispool = redispool
        self.url=attackurl
        self.rep=rep

    def GetStatus(self):
        print("正在获取网页状态码!")
        try:
            return str(self.rep.status_code)
        except Exception as e:
            print(e)
            return "None"

    def GetTitle(self):
        print("正在获取网页标题!")
        if self.rep != None:
            try:
                title=re.findall('<title>(.*?)</title>', self.rep.text)[0]
                return title
            except Exception as e:
                print(e)
                return None
        return None

    def GetDate(self):
        print("正在获取系统当前时间!")
        return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    def GetResponseHeader(self):
        print("正在获取网页响应头!")
        context = ""
        try:
            for key, val in self.rep.headers.items():
                context += (key + ": " + val + "\r\n")
            return context
        except Exception as e:
            print(e)
            return context

    def GetFinger(self):
        print("正在获取网站指纹及技术!")
        try:
            finger=WebPage(self.url, self.rep).info()
            return finger
        except Exception as e:
            print(e)
            return "Unknow"

    def PortScan(self):
        print("正在对目标进行端口扫描!")
        try:
            return get_message.PortScan(self.domain)
        except Exception as e:
            print(e)
            return "Unknow"

    def SenDir(self):
        print("正在进行敏感目录及文件探测!")
        try:
            return get_message.SenFileScan(self.domain,self.url)
        except Exception as e:
            print(e)
            return "None"

    def WebLogicScan(self):
        print("正在进行weblogic漏洞检测!")
        try:
            results=WebLogicScan.run(self.domain)
            with app.app_context():
                for result in results:
                    vulnerable, bugurl, bugname, bugdetail = result
                    if vulnerable:
                        bug = BugList(oldurl=self.domain, bugurl=bugurl, bugname=bugname,
                                      buggrade=redispool.hget('bugtype', bugname),
                                      payload=bugurl, bugdetail=bugdetail)
                        redispool.pfadd(redispool.hget('bugtype', bugname), bugurl)
                        redispool.pfadd(bugname, bugurl)
                        db.session.add(bug)
                db.session.commit()
        except Exception as e:
            print(e)
            pass

    def AngelSwordMain(self):
        print("正在使用碎遮内置POC进行漏洞检测!")
        try:
            selfpocscan.AngelSwordMain(self.url)
        except Exception as e:
            print(e)
            pass



if __name__=='__main__':
    # redispool=redis.ConnectionPool(host='127.0.0.1',port=6379, decode_responses=True)
    # redispool = redis.Redis(connection_pool=ImportToRedis.redisPool)
    try:
        rep=requests.get(url="http://testphp.vulnweb.com",headers=core.GetHeaders(),timeout=10)
        test=GetBaseMessage("testphp.vulnweb.com","http://testphp.vulnweb.com",rep)
        # test.AngelSwordMain()
        # print(test.GetStatus())
        # print(test.GetTitle())
        # print(test.GetResponseHeader())
        print(test.GetFinger())
        # print(test.PortScan())
        # print(test.SenDir())

    except Exception as e:
        print(e)
        pass

