import get_message
from init import redispool

class DomainMessage:
    def __init__(self,domain):
        self.domain=domain
        self.redispool=redispool
        self.TrueDomain=self.domain.split('.',1)[1]

    def GetSubDomain(self):
        print("get subdomain")
        SubDomainBurst=get_message.SubDomainBurst(self.TrueDomain,self.redispool)
        SubDomainOnline=get_message.GetSubDomain(self.domain)
        SubDomain=SubDomainBurst+SubDomainOnline
        return SubDomain

    def GetWhoisMessage(self):
        print("get whois message")
        return get_message.GetWhois(self.TrueDomain)

    def GetBindingIP(self):
        print("get binding ip")
        return get_message.GetBindingIP(self.domain)

    def GetSiteStation(self):
        print("get sitestation")
        return get_message.GetSiteStation(self.domain)

    def GetRecordInfo(self):
        print("get recordinfo")
        return get_message.GetRecordInfo(self.domain)

    def FindDomainAdd(self):
        print("find domain addr")
        return get_message.FindDomainAdd(self.domain)

if __name__=='__main__':
    test=DomainMessage("www.runoob.com")
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
