import requests
from lxml import etree
import nmap
import core
import re
from multiprocessing.pool import ThreadPool
import socket
import urllib3
from init import app
from exts import db
from models import BugList
from init import redispool
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
    """
    get_whois函数爬取http://whois.bugscaner.com/网站的英文搜索结果，并以字符串的方式将结果返回
    需要传入一个合法的域名domain
    爬取使用的requests 和 xpath 库
    :param domain:
    :return:
    """
    whois_url = 'http://whois.bugscaner.com/'
    try:
        rep = requests.get(whois_url + domain, headers=core.GetHeaders(), timeout=4.0)
        rep = etree.HTML(rep.text)
        data = rep.xpath('//div[@class="stats_table_91bf7bf"]/b[not(@style)]/text()')[0:19]
        str = "\n".join(data)
    except:
        str = None
        pass
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
    attacklist=[]
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
            
    if len(attacklist) > 0:
        attacklist[0] = "http://" + attacklist[0]
    return "\nhttp://".join(attacklist)


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
        str=""
        pass
    return str


'''
域名备案DNICP（Domain Name Internet Content Provider）
备案信息分为两种，一种是IPC备案信息查询，一种是公安部备案信息查询。
在中华人民共和国境内提供非经营性互联网信息服务，应当办理备案。
因此可以通过网站查询获取域名的备案信息。
在线查询网站：http://www.beianbeian.com

上面这个备案网站不能用了 ，换成站长之家备案在线查询 https://icp.chinaz.com/
'''


def GetRecordInfo(domain):
    '''
    返回域名的备案信息
    :param domain:
    :return:
    '''
    icpurl='https://icp.chinaz.com/'+domain
    context=""
    try:
        rep = requests.get(icpurl, headers=core.GetHeaders(),timeout=4)
        rep = etree.HTML(rep.text)
        companyname = rep.xpath('//ul[@id="first"]/li/p/a/text()')[0]
        type = rep.xpath('//ul[@id="first"]/li/p/strong/text()')[0]
        icpnum = rep.xpath('//ul[@id="first"]/li/p/font/text()')[0]
        wwwname = rep.xpath('//ul[@id="first"]/li/p/text()')[2]
        wwwurl = rep.xpath('//ul[@id="first"]/li/p/text()')[3]
        icpdate = rep.xpath('//ul[@id="first"]/li/p/text()')[11]
        context='''主办单位名称:{}\n主办单位性质:{}\n网站备案许可证号:{}\n网站名称:{}\n网站首页地址:{}\n审核时间:{}\n'''.format(companyname,type,icpnum,wwwname,wwwurl,icpdate)
    except Exception as e:
        pass
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
    return "\n".join(text)


'''
多线程
'''


def UrlRequest(url):
    try:
        r = requests.get(url, headers=core.GetHeaders(), timeout=1.0, verify=False)
        if r.status_code == 200 or r.status_code==403:
            return url
    except Exception:
        pass

def SubDomainBurst(true_domain,redispool):
    """
    子域名爆破
    从字典读取子域名构造新的url进行访问，若返回状态码为200，则返回可攻击列表attack_list
    :param true_domain:
    :return:
    """
    pools = 20
    urlList = []
    for i in range(0, redispool.llen("SubScan")):
        url="http://{}.{}".format(redispool.lindex("SubScan", i),true_domain)
        urlList.append(url)
    pool = ThreadPool(pools)
    SubDomain = pool.map(UrlRequest, urlList)
    pool.close()
    pool.join()
    return "\n".join(list(filter(None, SubDomain)))


def SenFileScan(domain,url):
    """
    敏感文件、目录扫描
    字典：dict\SEN_scan.txt
    :param domain:
    :param
    :return:
    """
    pools = 20
    urlList = []
    for i in range(0, redispool.llen("SenScan")):
        suffix=redispool.lindex("SenScan", i)
        senurl="{}/{}".format(url,suffix)
        urlList.append(senurl)
    pool = ThreadPool(pools)
    SenFileMessage = pool.map(UrlRequest, urlList)
    SenFileMessage2=""
    pool.close()
    pool.join()
    url404="{}/springbird404page".format(url)
    try:
        rep404=requests.get(url404, headers=core.GetHeaders(), timeout=3, verify=False).text
    except Exception as e:
        print("超时")
        rep404=str(e)
        pass
    if len(SenFileMessage)!=0:
        with app.app_context():
            print("Sen file and dir : \n")
            for url in SenFileMessage:
                try:
                    if url is None:
                        continue
                    rep = requests.get(url, headers=core.GetHeaders(), timeout=1, verify=False)
                    #添加404界面的判断，避免过多杂乱信息
                    if not core.is_similar_page(rep404,rep.text,radio=0.85):
                        print(url)
                        bug = BugList(oldurl=domain, bugurl=url, bugname="SenDir",buggrade=redispool.hget('bugtype', "SenDir"),payload=url, bugdetail=rep.text)
                        SenFileMessage2+=url+"\n"
                        redispool.pfadd(redispool.hget('bugtype', "SenDir"), url)
                        redispool.pfadd("SenDir", url)
                        db.session.add(bug)
                except Exception as e:
                    # print(e)
                    pass
            db.session.commit()
    return SenFileMessage2




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
    return "".join(list(filter(None, C_Message)))


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
    str=""
    url = "http://ip.yqie.com/ip.aspx?ip=" + domain
    try:
        rep = requests.get(url, headers=core.GetHeaders(),timeout=4)
        rep = etree.HTML(rep.text)
        context = rep.xpath('//div[@style="text-align: center; line-height: 30px;"]/text()')
        str = "\n".join(context)
    except Exception as e:
        print(e)
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
    print(FindDomainAdd('testphp.vulnweb.com'))
    # print(SenFileScan("testphp.vulnweb.com","http://testphp.vulnweb.com/"))
