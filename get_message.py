import requests
from lxml import etree
import nmap
import core
import re
from multiprocessing.pool import ThreadPool
import signal
import socket
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# 禁用安全警告

'''
whois get_message


简单介绍
    whois（读作“Who is”，非缩写）是用来查询域名的IP以及所有者等信息的传输协议。
    简单说，whois就是一个用来查询域名是否已经被注册，以及注册域名的详细信息的数据库（如域名所有人、域名注册商）。
    通过whois来实现对域名信息的查询。
    get_whois : http://whois.bugscaner.com/
'''


def GetWhois(domain):
    '''
    get_whois函数爬取http://whois.bugscaner.com/网站的英文搜索结果，并以字符串的方式将结果返回
    需要传入一个合法的域名domain
    爬取使用的requests 和 xpath 库
    :param domain:
    :return:
    '''
    whois_url = 'http://whois.bugscaner.com/'
    try:
        rep = requests.get(whois_url + domain, headers=core.GetHeaders(), timeout=2.0)
        rep = etree.HTML(rep.text)
        data = rep.xpath('//div[@class="stats_table_91bf7bf"]/b[not(@style)]/text()')[0:19]
        str = "\n".join(data)
    except:
        str = None
        pass
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
传入domain为 baidu.com形式
'''


def GetSubDomain(domain):
    chinaz_base_url = 'https://tool.chinaz.com/'
    chinaz_url = 'https://tool.chinaz.com/subdomain?domain=' + domain + '&page=1'
    attacklist = []
    while 1:
        try:
            rep = requests.get(chinaz_url, headers=core.GetHeaders(), timeout=2.0)
            rep = etree.HTML(rep.text)
            data = rep.xpath('//div[@class="w23-0"]/a[@href="javascript:"]/text()')
            attacklist.extend(data)
            next_url = rep.xpath('//a[@title="下一页"]/@href')[0]
            chinaz_url = chinaz_base_url + next_url
        except:
            break
    return attacklist


'''
CDN（content delivery network 或 content distribution network）即内容分发网络。
一些站点开启了CDN后就会隐藏掉自己的真实ip，在某些需要获取站点真实ip的工作中，这将是一个障碍
    这里使用查看解析历史的方法查找站点真实IP
    这是一种成功率极高的方法，站点可能创建之初并未添加CDN，这样就会存留下解析记录，通过查看解析历史可以寻找到服务器的真实ip
'''


def GetBindingIP(domain):
    '''
    返回域名的历史解析记录字符串
    :param domain:
    :return:
    '''
    pattern = re.compile('^\d+\.\d+\.\d+\.\d+$')
    ip138_url = 'https://site.ip138.com/' + domain
    try:
        rep = requests.get(ip138_url, headers=core.GetHeaders(), timeout=1.0)
        rep = etree.HTML(rep.text)
        if pattern.findall(domain):
            context = rep.xpath('//ul[@id="list"]/li/a/text()')
        else:
            context = rep.xpath('//div[@id="J_ip_history"]//a/text()')
        str = "\n".join(context)
    except:
        pass
    return str


'''
域名备案DNICP（Domain Name Internet Content Provider）
备案信息分为两种，一种是IPC备案信息查询，一种是公安部备案信息查询。
在中华人民共和国境内提供非经营性互联网信息服务，应当办理备案。
因此可以通过网站查询获取域名的备案信息。
在线查询网站：http://www.beianbeian.com
'''


def GetRecordInfo(domain):
    '''
    返回域名的备案信息
    :param domain:
    :return:
    '''
    check_url = 'http://www.beianbeian.com/s-0/' + domain + '.html'
    rep = requests.get(check_url, headers=core.GetHeaders())
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
    context = ""
    for i in zip(thead, tbody):
        context += ":".join(i) + "\n"
    if "没有符合条件的记录" in context:
        return None
    return context


def GetSiteStation(ip):
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
    url_2_base = 'http://stool.chinaz.com'
    url_2 = 'http://stool.chinaz.com/same?s=' + ip + '&page=1'
    text2 = []
    try:
        rep1 = requests.post(url_1, data=data, headers=core.GetHeaders(), timeout=2.0)
        rep1 = etree.HTML(rep1.text)
        text1 = rep1.xpath('//a[@class="domain"]/text()')
    except:
        text1 = []
        pass
    try:
        while 1:
            rep2 = requests.get(url_2, headers=core.GetHeaders(), timeout=2.0)
            rep2 = etree.HTML(rep2.text)
            new_list = rep2.xpath('//div[@class="w30-0 overhid"]/a/text()')
            if len(new_list) == 0:
                break
            text2 += new_list
            next_url = "".join(rep2.xpath('//a[@title="下一页"]/@href'))
            url_2 = url_2_base + next_url
    except:
        text2 = []
        pass
    text = list(set(text1).union(set(text2)))
    for i in text:
        if "屏蔽的关键字" in i:
            text.remove(i)
    str = "\n".join(text)
    return str


'''
多线程
'''



def UrlRequest(url):
    try:
        r = requests.get(url, headers=core.GetHeaders(), timeout=1.0, verify=False)
        if r.status_code == 200:
            return url+'\n'
    except Exception:
        pass


def SubDomainBurst(true_domain):
    """
    子域名爆破
    字典：dict\SUB_scan.txt
    从字典读取子域名构造新的url进行访问，若返回状态码为200，则返回可攻击列表attack_list
    :param true_domain:
    :return:
    """
    pools = 20
    urlList = []
    file = open(r"dict\SUB_scan.txt", "r")
    for line in file.readlines():
        url = 'http://' + line.strip('\n') + '.' + true_domain
        urlList.append(url)
    file.close()
    pool = ThreadPool(pools)
    SubDomainMessage=pool.map(UrlRequest, urlList)
    pool.close()
    pool.join()
    return "".join(list(filter(None,SubDomainMessage)))


def SenFileScan(domain):
    """
    敏感文件、目录扫描
    字典：dict\SEN_scan.txt
    :param domain:
    :param
    :return:
    """
    pools = 20
    urlList = []
    file = open(r"dict\SEN_scan.txt", "r", encoding='utf-8')
    for line in file.readlines():
        url = 'http://' + domain + line.replace("\n", '')
        urlList.append(url)
    file.close()
    pool = ThreadPool(pools)
    SenFileMessage=pool.map(UrlRequest, urlList)
    pool.close()
    pool.join()
    return "".join(list(filter(None,SenFileMessage)))


'''
敏感信息泄露
git泄露：当前大量开发人员使用git进行版本控制，对站点自动部署。如果配置不当,可能会将.git文件夹直接部署到线上环境。这就引起了git泄露漏洞。
hg泄露：当开发人员使用Mercurial进行版本控制，对站点自动部署。如果配置不当,可能会将.hg文件夹直接部署到线上环境。这就引起了hg泄露漏洞。
SVN泄露：当开发人员使用svn进行版本控制，对站点自动部署。如果配置不当,可能会将.svn文件夹直接部署到线上环境。这就引起了svn泄露漏洞。
'''


def InforLeakage(domain):
    """
    传入domain，构造新的url，进行访问，查看返回的状态码
    如果状态码为200或者403则代表存在信息泄露
    403：文件存在但没有访问权限
    :param domain:
    :return:
    """
    url = "http://" + domain
    urlGit = url + '/.git/'
    urlSVN = url + '/.svn/'
    urlHG = url + '/.hg/'
    try:
        Git = requests.get(urlGit, headers=core.GetHeaders(), timeout=2, verify=False)
    except Exception:
        pass
    GitCode = Git.status_code
    if GitCode == 200 or GitCode == 403:
        return domain + " 或许存在Git泄露"
    try:
        HG = requests.get(urlHG, headers=core.GetHeaders(), timeout=2, verify=False)
    except Exception:
        pass
    HGCode = HG.status_code
    if HGCode == 200 or HGCode == 403:
        return domain + "或许存在HG泄露"
    try:
        SVN = requests.get(urlSVN, headers=core.GetHeaders(), timeout=2, verify=False)
    except Exception:
        pass
    SVNCode = SVN.status_code
    if SVNCode == 200 or SVNCode == 403:
        return domain + "或许存在SVN泄露"
    return None


'''
NMap(Network Mapper)
调用nmap进行端口扫描，传入主机IP，实例化一个扫描对象nm
获取所有扫描协议的列表，输出所有协议扫描的开放端口以及相应端口对应的服务
'''


def PortScan(host):
    pattern = re.compile('^\d+\.\d+\.\d+\.\d+$')
    content = ""
    if not pattern.findall(host):
        host = socket.gethostbyname(host)
    nm = nmap.PortScanner()
    try:
        nm.scan(host, arguments='-Pn,-sS')
        for proto in nm[host].all_protocols():
            lport = list(nm[host][proto].keys())
            for port in lport:
                if nm[host][proto][port]['state'] == "open":
                    service = nm[host][proto][port]['name']
                    content += '[*]主机' + host + ' 协议：' + proto + '\t开放端口号：' + str(port) + '\t端口服务：' + service + "\n"
        return content
    except Exception as e:
        nmap.sys.exit(0)


def CScanConsole(ip):
    hostList = []
    ip = ip.split('.')
    pools = 20
    for tmpCip in range(1, 256):
        ip[-1] = str(tmpCip)
        host = ".".join(ip)
        hostList.append(host)
    pool = ThreadPool(pools)
    C_Message = pool.map(CScan, hostList)
    pool.close()
    pool.join()
    return "".join(list(filter(None,C_Message)))


def CScan(ip):
    """
    C段扫描
    状态码为200有title时返回title
    :param ip:
    :return:
    """
    try:
        rep = requests.get("http://" + ip, headers=core.GetHeaders(), timeout=1, verify=False)
        if rep.status_code == 200:
            title = re.findall(r'<title>(.*?)</title>', rep.text)
            if title:
                return "[T]" + ip + ' : ' + title[0] + "\n"
            else:
                return "[H]" + ip + " : have reason\n"
    except Exception as e:
        pass


'''
ip和域名真实地址查询
'''


def FindDomainAdd(domain):
    """
    查找域名真实地址
    :param domain:
    :return:
    """
    url = "http://ip.yqie.com/ip.aspx?ip=" + domain
    try:
        rep = requests.get(url, headers=core.GetHeaders())
        rep = etree.HTML(rep.text)
        context = rep.xpath('//div[@style="text-align: center; line-height: 30px;"]/text()')
        str = "\n".join(context)
    except:
        pass
    return str.lstrip()


def FindIpAdd(ip):
    """
    查找IP真实地址
    :param ip:
    :return:
    """
    str = ""
    url = "http://ip.yqie.com/ip.aspx?ip=" + ip
    try:
        rep = requests.get(url, headers=core.GetHeaders(), timeout=2)
        rep = etree.HTML(rep.text)
        context = rep.xpath('//input[@id="AddressInfo"]/@value')
        str = "\n".join(context)
    except:
        pass
    return str


if __name__ == "__main__":
    # 测试数据
    # print(GetBindingIP('202.202.157.110'))
    # print(GetSiteStation('202.202.157.110'))
    # print(CScanConsole('202.202.157.110'))
    # print(FindIpAdd('202.202.157.110'))
    # SubDomainBurst('baidu.com')
    # print(CScanConsole('202.202.157.110'))
    print(SenFileScan("www.baidu.com"))