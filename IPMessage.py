import get_message
import redis

class IPMessage:
    def __init__(self,ip):
        self.ip=ip

    def GetBindingIP(self):
        print("正在进行IP历史解析记录!")
        try:
            return get_message.GetBindingIP(self.ip)
        except Exception as e:
            print(e)
            return "None"

    def GetSiteStation(self):
        print("正在进行旁站查询!")
        try:
            return get_message.GetSiteStation(self.ip)
        except Exception as e:
            print(e)
            return "None"

    def CScanConsole(self):
        print("正在进行C段信息搜集!")
        try:
            return get_message.CScanConsole(self.ip)
        except Exception as e:
            print(e)
            return "Unknow"

    def FindIpAdd(self):
        print("正在查找IP地址查询")
        try:
            return get_message.FindIpAdd(self.ip)
        except Exception as e:
            print(e)
            return "None"

if __name__=='__main__':
    # test=IPMessage('202.202.157.110')
    url='202.202.157.110'
    test=IPMessage(url)
    print("end!")
    # print(test.GetBindingIP())
    # print(test.GetSiteStation())
    # print(test.CScanConsole())
    # print(test.FindIpAdd())