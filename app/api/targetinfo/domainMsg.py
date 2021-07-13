

'''
    域名信息收集:
        备案信息
        whois信息
        子域名
        物理地址
        CDN检测
        DNS历史解析记录
'''
class DomainMsg:
    def __init__(self):
        self.baseWhoisUrl='http://whois.bugscaner.com/'
        return

    def getWhoisMsg(self):
        # 获取whois 信息
        return

    def getBeianMsg(self):
        # 获取备案信息
        return

    def getSubDomainMsg(self):
        # 获取子域名信息
        return

    def getCDNMsg(self):
        # 获取CDN信息
        return

    def getDNSMsg(self):
        # 获取DNS解析记录
        return