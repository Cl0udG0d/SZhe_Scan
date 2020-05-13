import get_message
import redis
import ImportToRedis

class DomainMessage:
    def __init__(self,domain,redispool):
        self.domain=domain
        self.redispool=redispool
        self.TrueDomain=self.domain.split('.',1)[1]

    def GetSubDomain(self):
        SubDomainBurst=get_message.SubDomainBurst(self.TrueDomain,self.redispool)
        SubDomainOnline=get_message.GetSubDomain(self.domain)
        SubDomain=SubDomainBurst+SubDomainOnline
        print("111")
        return SubDomain

    def GetWhoisMessage(self):
        return get_message.GetWhois(self.TrueDomain)

    def GetBindingIP(self):
        return get_message.GetBindingIP(self.domain)

    def GetSiteStation(self):
        return get_message.GetSiteStation(self.domain)

    def GetRecordInfo(self):
        return get_message.GetRecordInfo(self.domain)

    def FindDomainAdd(self):
        return get_message.FindDomainAdd(self.domain)

if __name__=='__main__':
    redispool = redis.Redis(connection_pool=ImportToRedis.redisPool)
    test=DomainMessage("testphp.vulnweb.com",redispool)
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
