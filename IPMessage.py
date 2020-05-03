import get_message
import redis

class IPMessage:
    def __init__(self,ip):
        self.ip=ip

    def GetBindingIP(self):
        return get_message.GetBindingIP(self.ip)

    def GetSiteStation(self):
        return get_message.GetSiteStation(self.ip)

    def CScanConsole(self):
        return get_message.CScanConsole(self.ip)

    def FindIpAdd(self):
        return get_message.FindIpAdd(self.ip)

if __name__=='__main__':
    # test=IPMessage('202.202.157.110')
    url='202.202.157.110'
    test=IPMessage(url)
    print("end!")
    # print(test.GetBindingIP())
    # print(test.GetSiteStation())
    # print(test.CScanConsole())
    # print(test.FindIpAdd())