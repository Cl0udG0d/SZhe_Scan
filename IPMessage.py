import GetMessage
import re
from Init import redispool

class IPMessage:
    def __init__(self,ip):
        self.ip=ip

    def GetBindingIP(self):
        redispool.append("runlog", "正在获取{}IP历史解析记录!\n".format(self.ip))
        print("正在获取IP历史解析记录!")
        try:
            return GetMessage.GetBindingIP(self.ip)
        except Exception as e:
            print(e)
            return "None"

    def GetSiteStation(self):
        redispool.append("runlog", "正在进行{}旁站查询!\n".format(self.ip))
        print("正在进行旁站查询!")
        try:
            return GetMessage.GetSiteStation(self.ip)
        except Exception as e:
            print(e)
            return "None"

    def CScanConsole(self):
        redispool.append("runlog", "正在进行{}C段信息搜集!\n".format(self.ip))
        print("正在进行C段信息搜集!")
        try:
            return GetMessage.CScanConsole(self.ip)
        except Exception as e:
            print(e)
            return "Unknow"

    def FindIpAdd(self):
        redispool.append("runlog", "正在查找{}IP地址\n".format(self.ip))
        print("正在查找IP地址查询")
        try:
            return GetMessage.FindIpAdd(self.ip)
        except Exception as e:
            print(e)
            return "None"

if __name__=='__main__':
    url="202.202.157.110"
    pattern = re.compile('^\d+\.\d+\.\d+\.\d+(:(\d+))?$')
    # 判断IP是否存在端口
    if pattern.findall(url) and ":" in url:
        infourl = url.split(":")[0]
    else:
        infourl = url
    print(infourl)
    test=IPMessage(infourl)
    print("end!")
    print(test.GetBindingIP())
    print(test.GetSiteStation())
    print(test.CScanConsole())
    print(test.FindIpAdd())