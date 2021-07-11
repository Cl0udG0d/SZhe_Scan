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
        # 获取 target
        if self.url.startswith("http"):
            self.target='/'.join(self.url.split('/')[0:3])
        else:
            self.target=self.useRepCheckTarget()
        return

    def getDomain(self):
        # 获取 domain
        if self.url.startswith("http://") or self.url.startswith("https://"):

        return

    def getTargetMsg(self):
        # 获取目标的基础信息
        return

    def getResponse(self):
        # 获取响应
        self.rep = normalReq(self.target)
        return

    def getStatus(self):
        # 获取状态码
        return self.rep.status_code

    def getTitle(self):
        # 获取目标标题
        value=re.findall('<title>(.*?)</title>', self.rep.text)
        if type(value) is list:
            title=value[0]
        else:
            title='no title'
        return title

    def getDate(self):
        # 获取当前时间
        return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    def getRepHeaderMsg(self):
        # 响应头获取
        context = ""
        for key, val in self.rep.headers.items():
            context += (key + ": " + val + "\r\n")
        return context

    def getFinger(self):
        # 指纹识别
        return

    def getTargetPort(self):
        # 端口识别
        return

    def getTargetSensitiveMsg(self):
        # 敏感信息
        return

    def checkDomain(self):
        # check domain or IP
        pass

    def useRepCheckTarget(self):
        # 利用 rep 检测 http or https 
        if '/' in self.url:
            tempTarget=self.url.split('/')[0]
        else:
            tempTarget=self.url

        return
