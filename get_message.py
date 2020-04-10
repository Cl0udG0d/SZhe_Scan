import requests
from lxml import etree
import time
import zlib
import json

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


'''
域名备案DNICP（Domain Name Internet Content Provider）
备案信息分为两种，一种是IPC备案信息查询，一种是公安部备案信息查询。
在中华人民共和国境内提供非经营性互联网信息服务，应当办理备案。
因此可以通过网站查询获取域名的备案信息。
在线查询网站：http://www.beianbeian.com
'''


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




def get_siteStation(ip):
    """
    旁站查询
    查询网站1：https://www.webscan.cc/search/
    查询网站2：http://stool.chinaz.com
    查询网站3：http://www.114best.com/ip/114.aspx
    :param ip:
    :return:
    """
    data = {'domain': ip}
    url_1 = 'https://www.webscan.cc/search/'
    rep1 = requests.post(url_1, data=data, headers=headers)
    rep1 = etree.HTML(rep1.text)
    text1 = rep1.xpath('//a[@class="domain"]/text()')

    url_2_base = 'http://stool.chinaz.com'
    url_2 = 'http://stool.chinaz.com/same?s=' + ip + '&page=1'
    text2 = []
    while 1:
        rep2 = requests.get(url_2, headers=headers)
        rep2 = etree.HTML(rep2.text)
        new_list = rep2.xpath('//div[@class="w30-0 overhid"]/a/text()')
        if len(new_list) == 0:
            break
        text2 += new_list
        next_url = "".join(rep2.xpath('//a[@title="下一页"]/@href'))
        url_2 = url_2_base + next_url

    url_3 = 'http://www.114best.com/ip/114.aspx?w=' + ip
    rep3 = requests.get(url_3, headers=headers)
    rep3 = etree.HTML(rep3.text)
    text3 = rep3.xpath('//div[@id="rl"]/span/text()')
    text3 = [x.strip() for x in text3]
    text = list(set(text1).union(set(text2)).union(set(text3)))
    for i in text:
        if "屏蔽的关键字" in i:
            text.remove(i)
    str = "\n".join(text)
    return str



def Subdomain_burst(domain, filename):
    '''
    子域名爆破
    字典：dict\SUB_scan.txt
    从字典读取子域名构造新的url进行访问，若返回状态码为200，则写入文件夹。
    :param domain:
    :param filename:
    :return:
    '''
    file = open(r"dict\SUB_scan.txt", "r")
    resultFile = open(filename, "a+")
    for line in file.readlines():
        url = 'http://' + line.replace("\n", '.' + domain)
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            resultFile.write(url + "\n")


def sensitive_scan(domain, filename):
    '''
    敏感文件、目录扫描
    字典：dict\SEN_scan.txt
    :param domain:
    :param filename:
    :return:
    '''
    file = open(r"dict\SEN_scan.txt", "r", encoding='utf-8')
    resultFile = open(filename, "a+")
    for line in file.readlines():
        url = 'http://' + domain + line.replace("\n", '')
        r = requests.get(url, headers=headers, allow_redirects=False)
        if r.status_code == 200:
            resultFile.write(url + "\n")

def whatweb(url):
    try:
        response = requests.get(url,headers=headers,verify=False,timeout=3)
    except:
        pass
    whatweb_dict = {"url": response.url, "text": response.text, "headers": dict(response.headers)}
    whatweb_dict = json.dumps(whatweb_dict)
    whatweb_dict = whatweb_dict.encode()
    whatweb_dict = zlib.compress(whatweb_dict)
    data = {"info": whatweb_dict}
    return requests.post("http://whatweb.bugscaner.com/api.go", files=data)
'''
传入url形式为http://www.dedecms.com/,requests能直接访问的网址
返回数据为json格式的识别结果，每天在线识别的次数上限为1500次
后续完善本地CMS指纹识别
调用自bugscaner博客出品，在线指纹识别,在线cms识别小插件--在线工具API
http://whatweb.bugscaner.com/look/
'''
def cms_finger(url):
    request = whatweb(url)
    print(u"今日识别剩余次数")
    print(request.headers["X-RateLimit-Remaining"])
    print(u"识别结果")
    print(request.json())


# 测试数据
# get_whois("shkls.com")
# get_sundomain("baidu.com")
# get_ip("baidu.com")
# get_recordinfo("baidu.com")
# get_siteStation("172.217.27.142")

# Subdomain_burst("baidu.com", "dict\test1.txt")
# sensitive_scan("www.anantest.com", "dict\test2.txt")

#cms_finger("http://www.dedecms.com/")

