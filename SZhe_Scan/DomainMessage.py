import get_message
from init import redispool

class DomainMessage:
    def __init__(self,domain):
        self.domain=domain
        self.redispool=redispool
        self.TrueDomain=self.domain.split('.',1)[1]

    def GetSubDomain(self):
        print("正在使用主动与被动方式获取目标子域名!")
        try:
            SubDomainBurst=get_message.SubDomainBurst(self.TrueDomain,self.redispool)
            SubDomainOnline=get_message.GetSubDomain(self.domain)
            SubDomain=SubDomainBurst+SubDomainOnline
            return SubDomain
        except Exception as e:
            print(e)
            return "None"

    def GetWhoisMessage(self):
        print("正在获取网站Whois信息!")
        try:
            return get_message.GetWhois(self.TrueDomain)
        except Exception as e:
            print(e)
            return "None"

    def GetBindingIP(self):
        print("正在获取域名历史解析记录 :D")
        try:
            return get_message.GetBindingIP(self.domain)
        except Exception as e:
            print(e)
            return "None"

    def GetSiteStation(self):
        print("正在进行旁站查询 :)")
        try:
            return get_message.GetSiteStation(self.domain)
        except Exception as e:
            print(e)
            return "None"

    def GetRecordInfo(self):
        print("正在获取域名的公开备案信息 :-)")
        try:
            return get_message.GetRecordInfo(self.domain)
        except Exception as e:
            print(e)
            return "None"

    def FindDomainAdd(self):
        print("正在获取域名映射的真实地址!")
        try:
            return get_message.FindDomainAdd(self.domain)
        except Exception as e:
            print(e)
            return "None"

if __name__=='__main__':
    test=DomainMessage("www.nowcoder.com")
    try:
        print(test.GetSiteStation())
        print(test.GetBindingIP())
        print(test.GetWhoisMessage())
        print(test.GetRecordInfo())
        print(test.FindDomainAdd())
        print(test.GetSubDomain())
    except Exception as e:
        print(e)
        pass
