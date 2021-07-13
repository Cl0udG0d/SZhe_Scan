import re
import time
from . import getMsgUnit,Wappalyzer
import socket
from app.utils.selfrequests import normalReq,checkReq

'''
    基础信息收集:
            目标网址
            域名
            响应
            状态码
            标题
            时间
            响应头
            指纹识别
            端口识别
            被动信息收集中的敏感信息收集
'''
class TargetMsg:
    def __init__(self,url):
        self.url=url
        self.domain=self.getDomain()
        self.target=self.getTarget()
        self.isDomain=self.checkDomain()
        self.rep=None
        self.havaWaf=False

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
            return self.url.split('/')[2] if ':' not in self.url else self.url.split('/')[2].split(':')[0]
        elif '/' in self.url:
            return self.url.split('/')[0] if ':' not in self.url else self.url.split('/')[0].split(':')[0]
        else:
            return self.url if ':' not in self.url else self.url.split(':')[0]

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
        finger = Wappalyzer.WebPage(self.target, self.rep)
        return finger.info()

    def getTargetPort(self):
        # 端口识别
        host=socket.gethostbyname(self.domain) if self.isDomain else self.domain
        content=getMsgUnit.PortScan(host)
        return content

    # def getTargetSensitiveMsg(self):
        # 被动信息收集中的敏感信息
        # 是否存在WAF JS敏感信息 WAF识别 github敏感信息泄露 邮箱收集 物理地址 旁站查询
        # return


    def getTargetSenInJs(self):
        # js敏感信息获取
        return

    def getTargetWafMsg(self):
        # 目标WAF信息识别
        return

    def getGithubSenMsg(self):
        # Github 敏感信息获取
        return

    def getTargetEmail(self):
        # 邮箱收集
        return

    def getSiteStation(self):
        # 旁站查询
        return

    def checkDomain(self):
        # check domain or IP
        # pattern = re.compile('^\d+\.\d+\.\d+\.\d+(:(\d+))?$')
        pattern = re.compile('^\d+\.\d+\.\d+\.\d+$')
        return False if pattern.findall(self.domain) else True

    def checkHavaWaf(self):
        # 检测是否存在 waf

        return

    def useRepCheckTarget(self):
        # 利用 rep 检测 http or https 
        if '/' in self.url:
            tempTarget=self.url.split('/')[0]
        else:
            tempTarget=self.url
        try:
            tempurl="http://"+tempTarget
            rep1=checkReq(url=tempurl)
            return tempurl
        except:
            pass
        try:
            tempurl = "https://"+tempTarget
            rep2=checkReq(url=tempurl)
            return tempurl
        except:
            pass
        raise ("目标WEB端口无响应或URL格式错误")
