import re
import time

from app.utils.selfrequests import normalReq

class TargetMsg:
    def __init__(self,url):
        self.url=url
        self.domain=self.getDomain()
        self.target=self.getTarget()
        self.isDomain=self.checkDomain()
        self.rep=None

        return

    def getTarget(self):
        self.rep=normalReq(self.target)

    def getDomain(self):
        return

    def getResponse(self):
        self.rep = normalReq(self.target)
        return

    def getStatus(self):

        return self.rep.status_code

    def getTitle(self):
        value=re.findall('<title>(.*?)</title>', self.rep.text)
        if type(value) is list:
            title=value[0]
        else:
            title='no title'
        return title

    def GetDate(self):
        print("正在获取系统当前时间!")
        return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    def getTargetPort(self):
        return

    def getTargetSensitiveMsg(self):
        return

    def checkDomain(self):
        pass
