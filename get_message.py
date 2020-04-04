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
这里被动子域名
'''
def get_sundomain(domain):


#测试数据
# get_whois("shkls.com")
