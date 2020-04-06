import requests
from lxml import etree
import time

headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6) ",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "en-us",
           "Connection": "keep-alive",
           "Accept-Charset": "GB2312,utf-8;q=0.7,*;q=0.7"}
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
    whois_url = 'http://whois.bugscaner.com/'
    rep = requests.get(whois_url + domain)
    rep = etree.HTML(rep.text)
    data = rep.xpath('//div[@class="stats_table_91bf7bf"]/b[not(@style)]/text()')[0:19]
    str = "\n".join(data)
    # print(str)
    return str


'''
每个域名的情况都不一样，，比如一个被爬虫收录很差的域名，我们采用搜索引擎搜索的话很难搜集到全部的子域名
    这里使用在线网站搜集和必应搜索引擎搜集两种搜集方式实现被动子域名搜集
    在线子域名搜集：https://tool.chinaz.com/subdomain
                   https://site.ip138.com/
    必应搜索引擎搜集：https://cn.bing.com/  必应爬取前15页
    bing 模块未完成
    返回获取的子域名字符串
'''


def get_sundomain(domain):
    chinaz_base_url = 'https://tool.chinaz.com/'
    chinaz_url = 'https://tool.chinaz.com/subdomain?domain=' + domain + '&page=1'
    ip138_url = 'https://site.ip138.com/' + domain + '/domain.htm'
    context = []
    while 1:
        rep = requests.get(chinaz_url, headers=headers)
        rep = etree.HTML(rep.text)
        try:
            data = rep.xpath('//div[@class="w23-0"]/a[@href="javascript:"]/text()')
            context.extend(data)
            next_url = rep.xpath('//a[@title="下一页"]/@href')[0]
            chinaz_url = chinaz_base_url + next_url
        except:
            break
    rep = requests.get(ip138_url, headers=headers)
    rep = etree.HTML(rep.text)
    try:
        data = rep.xpath('//div[@class="panel"]//a/text()')
        context.extend(data)
    except:
        pass
    new_context = list(set(context))
    str = "\n".join(new_context)
    return str


'''
CDN（content delivery network 或 content distribution network）即内容分发网络。
一些站点开启了CDN后就会隐藏掉自己的真实ip，在某些需要获取站点真实ip的工作中，这将是一个障碍
    这里使用查看解析历史的方法查找站点真实IP
    这是一种成功率极高的方法，站点可能创建之初并未添加CDN，这样就会存留下解析记录，通过查看解析历史可以寻找到服务器的真实ip
'''


def get_ip(domain):
    '''
    返回域名的历史解析记录字符串
    :param domain:
    :return:
    '''

    ip138_url = 'https://site.ip138.com/' + domain
    rep = requests.get(ip138_url, headers=headers)
    rep = etree.HTML(rep.text)
    context = rep.xpath('//div[@id="J_ip_history"]//a/text()')
    str = "\n".join(context)
    return str


def get_recordinfo(domain):
    '''
    返回域名的备案信息
    :param domain:
    :return:
    '''
    check_url = 'http://www.beianbeian.com/s-0/' + domain + '.html'
    rep = requests.get(check_url, headers=headers)
    rep = etree.HTML(rep.text)
    thead = rep.xpath('//table[@class="layui-table res_table"]//th/text()')
    td_4 = "".join(rep.xpath('//tbody[@id="table_tr"]//td[4]/a/text()'))
    td_6 = " ".join(rep.xpath('//tbody[@id="table_tr"]//td[6]/a/text()'))
    td_8 = "".join(rep.xpath('//tbody[@id="table_tr"]//td[8]/a/text()'))
    tbody = rep.xpath('//tbody[@id="table_tr"]//td[1]/text()')
    tbody.append("".join(rep.xpath('//tbody[@id="table_tr"]//td[2]/text()')))
    tbody.append("".join(rep.xpath('//tbody[@id="table_tr"]//td[3]/text()')))
    tbody.append(td_4)
    tbody.append("".join(rep.xpath('//tbody[@id="table_tr"]//td[5]/text()')))
    tbody.append(td_6)
    tbody.append("".join(rep.xpath('//tbody[@id="table_tr"]//td[7]/text()')))
    tbody.append(td_8)
    # context2[3] = context3[0]+context3[1]
    # context2[4] = homeURL
    for i in zip(thead, tbody):
        print(":".join(i))


# 测试数据
# get_whois("shkls.com")
# get_sundomain("baidu.com")
# get_ip("baidu.com")
# get_recordinfo("baidu.com")
