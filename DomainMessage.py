import get_message


class DomainMessage:
    def __init__(self,domain):
        self.domain=domain
        self.TrueDomain=self.domain.split('.',1)[1]

    def GetSubDomain(self):
        SubDomainBurst=get_message.SubDomainBurst(self.TrueDomain)
        SubDomainOnline=get_message.GetSubDomain(self.domain)
        SubDomain=list(set(SubDomainBurst.extend(SubDomainOnline)))
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
    test=DomainMessage("github.com")
    print(test.GetSiteStation())
    print(test.GetBindingIP())
    print(test.GetWhoisMessage())
    print(test.GetRecordInfo())
    print(test.FindDomainAdd())
    print(test.GetSubDomain())
