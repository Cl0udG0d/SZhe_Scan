import requests
import core
import re
import time
from Wappalyzer import WebPage
import get_message
import redis

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
    def __init__(self,url):
        self.domain=url
        try:
            if not (url.startswith("http://") or url.startswith("https://")):
                self.url = "http://" + url
            else:
                self.url = url
            self.rep = requests.get(self.url, headers=core.GetHeaders(), timeout=3)
        except:
            pass
        finally:
            if self.rep==None:
                self.url="https://"+url
                self.rep = requests.get(self.url, headers=core.GetHeaders(), timeout=3)

    def GetStatus(self):
        return self.rep.status_code

    def GetTitle(self):
        if self.rep!=None:
            title = re.findall('<title>(.*?)</title>', self.rep.text)
            return title
        return None

    def GetDate(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def GetResponse(self):
        return self.rep.headers

    def GetFinger(self):
        return WebPage(self.url,self.rep).info()

    def PortScan(self):
        return get_message.PortScan(self.domain)
    def SenMessage(self):
        vulnerable, result=get_message.InforLeakage(self.domain)
        return vulnerable,result
    def SenDir(self):
        result=get_message.SenFileScan(self.domain)
        return result


if __name__=='__main__':
    test=GetBaseMessage("www.baidu.com")
    # print(test.GetDate())
    # print(test.GetResponse())
    # print(test.GetTitle())
    # print(test.GetStatus())
    # print(test.GetFinger())
    # print(test.PortScan())