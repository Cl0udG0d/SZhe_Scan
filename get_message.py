import requests
from lxml import etree

'''
whois get_message
简单介绍
    whois（读作“Who is”，非缩写）是用来查询域名的IP以及所有者等信息的传输协议。
    简单说，whois就是一个用来查询域名是否已经被注册，以及注册域名的详细信息的数据库（如域名所有人、域名注册商）。
    通过whois来实现对域名信息的查询。
    get_whois : http://whois.bugscaner.com/
'''
def get_whois(domain):
    '''
    get_whois函数爬取http://whois.bugscaner.com/网站的英文搜索结果，并以字符串的方式将结果返回
    需要传入一个合法的域名domain
    爬取使用的requests 和 xpath 库
    :param domain:
    :return:
    '''
    whois_url='http://whois.bugscaner.com/'
    rep=requests.get(whois_url+domain)
    rep = etree.HTML(rep.text)
    data=rep.xpath('//div[@class="stats_table_91bf7bf"]/b[not(@style)]/text()')[0:19]
    str="\n".join(data)
    # print(str)
    return str

'''
每个域名的情况都不一样，，比如一个被爬虫收录很差的域名，我们采用搜索引擎搜索的话很难搜集到全部的子域名
    这里使用在线网站搜集和必应搜索引擎搜集两种搜集方式实现被动子域名搜集
    在线子域名搜集：https://tool.chinaz.com/subdomain
    必应搜索引擎搜集：https://cn.bing.com/
'''
def get_sundomain(domain):

    base_url='https://tool.chinaz.com/'
    chinaz_url = 'https://tool.chinaz.com/subdomain?domain=' + domain + '&page=1'
    context=[]
    while 1:
        rep = requests.get(chinaz_url)
        rep = etree.HTML(rep.text)
        data = rep.xpath('//div[@class="w23-0"]/a[@href="javascript:"]/text()')
        str = "\n".join(data)
        print(str)
        try:
            next_url = rep.xpath('//a[@title="下一页"]/@href')[0]
            chinaz_url=base_url+next_url
        except:
            break



#测试数据
# get_whois("shkls.com")
get_sundomain("baidu.com")