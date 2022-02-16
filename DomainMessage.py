import GetMessage
from init import redispool


class DomainMessage:
    def __init__(self, domain):
        self.domain = domain
        self.redispool = redispool
        self.TrueDomain = self.domain.split('.', 1)[1]

    def GetSubDomain(self):
        redispool.append("runlog", "正在使用主动与被动方式获取{}目标子域名!\n".format(self.domain))
        print("正在使用主动与被动方式获取目标子域名!")
        try:
            SubDomainBurst = GetMessage.SubDomainBurst(self.TrueDomain, self.redispool)
            SubDomainOnline = GetMessage.GetSubDomain(self.domain)
            SubDomain = SubDomainBurst + SubDomainOnline
            return SubDomain
        except Exception as e:
            print(e)
            return "None"

    def GetWhoisMessage(self):
        redispool.append("runlog", "正在获取网站{}Whois信息!\n".format(self.domain))
        print("正在获取网站Whois信息!")
        try:
            return GetMessage.GetWhois(self.TrueDomain)
        except Exception as e:
            print(e)
            return "None"

    def GetBindingIP(self):
        redispool.append("runlog", "正在获取{}域名历史解析记录 :D\n".format(self.domain))
        print("正在获取域名历史解析记录 :D")
        try:
            return GetMessage.GetBindingIP(self.domain)
        except Exception as e:
            print(e)
            return "None"

    def GetSiteStation(self):
        redispool.append("runlog", "正在进行{}旁站查询 :)\n".format(self.domain))
        print("正在进行旁站查询 :)")
        try:
            return GetMessage.GetSiteStation(self.domain)
        except Exception as e:
            print(e)
            return "None"

    def GetRecordInfo(self):
        redispool.append("runlog", "正在获取{}域名的公开备案信息 :-)\n".format(self.domain))
        print("正在获取域名的公开备案信息 :-)")
        try:
            return GetMessage.GetRecordInfo(self.domain)
        except Exception as e:
            print(e)
            return "None"

    def FindDomainAdd(self):
        redispool.append("runlog", "正在获取{}域名映射的真实地址!\n".format(self.domain))
        print("正在获取域名映射的真实地址!")
        if "/" in self.domain:
            host=self.domain.split("/")[0]
        else:
            host=self.domain
        try:
            return GetMessage.FindDomainAdd(host)
        except Exception as e:
            print(e)
            return "None"


if __name__ == '__main__':
    test = DomainMessage("www.nowcoder.com")
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
