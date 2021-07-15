from app.utils.selfrequests import normalReq
from lxml import etree

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
    def __init__(self,domain):
        self.domain=domain
        return

    def getWhoisMsg(self):
        # 获取whois 信息
        whois_url = 'http://whois.bugscaner.com/'
        rep = normalReq(url=whois_url + self.domain)
        rep = etree.HTML(rep.text)
        data = rep.xpath('//div[@class="stats_table_91bf7bf"]/b[not(@style)]/text()')
        str = "\n".join(data[0:19]) if len(data)!=0 else "Not Msg"
        return str


    def getBeianMsg(self):
        # 获取备案信息
        icpurl = 'https://icp.chinaz.com/' + self.domain
        rep = normalReq(url=icpurl)
        rep = etree.HTML(rep.text)
        flag=rep.xpath('//ul[@id="first"]')
        if flag:
            companyname = rep.xpath('//ul[@id="first"]/li/p/text()')[0]
            type = rep.xpath('//ul[@id="first"]/li/p/strong/text()')[0]
            icpnum = rep.xpath('//ul[@id="first"]/li/p/font/text()')[0]
            wwwname = rep.xpath('//ul[@id="first"]/li/p/text()')[1]
            wwwurl = rep.xpath('//ul[@id="first"]/li/p/text()')[2]
            icpdate = rep.xpath('//ul[@id="first"]/li/p/text()')[3]
            context = '''主办单位名称:{}\n主办单位性质:{}\n网站备案许可证号:{}\n网站名称:{}\n网站首页地址:{}\n审核时间:{}\n'''.format(companyname,type,icpnum,wwwname,wwwurl,icpdate)
        else:
            context="无备案信息或参数错误"
        return context

    def getSubDomainMsg(self):
        # 获取子域名信息 字典+在线
        return

    def getCDNMsg(self):
        # 获取CDN信息
        return



if __name__ == '__main__':
    icpurl = 'https://icp.chinaz.com/' + '127.0.0.1'
    rep = normalReq(url=icpurl)
    rep = etree.HTML(rep.text)
    flag = rep.xpath('//ul[@id="first"]')
    if flag:
        print(flag)