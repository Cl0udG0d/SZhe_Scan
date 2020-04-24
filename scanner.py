import signal
import multiprocessing
import time
import get_message
import re
import signal
import multiprocessing
import SpiderGetUrl
import get_message
'''
ip和域名进入不同的调度函数扫描
====进程是资源分配的单位，线程是操作系统调度的单位====
获取target目标url，进行同域名下的及网页中的输入源搜集
scan函数传入扫描urls，单个或多个url，进入输入源获取函数
输入形式都可，进行自主判断
               创建进程池，多进程进行扫描，实现并行效果，默认进程为10,配置文件config.py
输入源获取->清洗->进入扫描队列->通过扫描器黑盒扫描->扫描信息存储进入MySQL数据库
                                               ->扫描信息回显在页面上

               ->进入待选队列->选择扫描->进入扫描队列---
                            ->不选择扫描->存储到数据库中
                                       ->回显在页面上
                ->队列为空，结束扫描
                ->队列不为空，显示实时扫描进度
清洗->将url修改为每个函数能接收的形式
    ->域名不在扫描范围内的放入待选队列，手动确认后加入扫描队列
扫描器黑盒扫描->信息搜集(get_message)
             ->sql注入检测
             ->XSS检测
             ->命令执行检测
             ->文件包含漏洞检测
             ->登录界面发现->弱密码爆破登录
             ->FUZZ模块

信息搜集->被动信息搜集
       ->主动信息搜集
'''
def init():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def index(queue):
    url=queue.get()
    urllist=GetUrlToQueue(url)

    print(url)
    return True,str(url)
'''
子域名搜集(被动搜集+主动搜集)->子域名页面url深度爬取(提取在子域名范围内的url)->加入队列
'''
def GetUrlToQueue(url):

    list1=get_message.GetSubDomain(url)
    # list2=

def UrlScan(urls):
    vulnerables = [] #存储有漏洞的url
    results = {} #存储扫描结果
    max_processes = 10
    queue = multiprocessing.Manager().Queue()
    pool = multiprocessing.Pool(max_processes, init)
    for url in urls:
        queue.put(url)
    def callback(result):
        results[result[1]] = result[0]
    #检测队列是否为空，空的话证明没有需要扫描的url了，停止扫描，否则进入index函数进行url调度扫描
    #result存储两个结果，一个是是否存在漏洞，一个是漏洞的类型
    try:
        while not queue.empty():
            pool.apply_async(index,(queue,),callback=callback)
            time.sleep(0.5)
    except Exception:
        pool.terminate()
        pool.join()
    else:
        pool.close()
        pool.join()
    for url, result in results.items():
        if result:
            # print(str(result)+url)
            vulnerables.append((url, result))
    return vulnerables

#当为ip地址时返回true，否则认为是域名
def Domain_IP_Check(url):
    pattern = re.compile('^\d+\.\d+\.\d+\.\d+$')
    if pattern.findall(url):
        return True
    else:
        return False
'''
对输入IP进行信息搜集
获取同服IP站点列表，IP旁站查询

'''
def IP_Message(ip):
    BindingDomain=get_message.get_ip(ip)
    GetSiteStation=get_message.get_siteStation(ip)

    return None

'''
对输入IP进行信息搜集，信息存入数据库
最后对attack_queue队列中的页面url深度搜集，进入漏洞扫描
漏洞扫描结果存入数据库
页面按规定显示扫描结果
'''
def IP_Console(ip):
    max_processes = 3
    attack_queue = multiprocessing.Manager().Queue()
    pool = multiprocessing.Pool(max_processes, init)
    attack_queue.put(ip)
    pool.apply_async(IP_Message, (ip,))
    pool.apply_async(SpiderGetUrl.depth_get, (ip, attack_queue,))
    pool.close()
    pool.join()
    print("end")
    return None

'''
对于域名domain收集信息：
    whois，解析IP，备案信息，旁站，cmd指纹
'''
def Domain_Message(domain,url):
    WhoisMessage=get_message.get_whois(domain)
    BindingIP=get_message.get_ip(domain)
    DomainRecordinfo=get_message.get_recordinfo(domain)
    SiteStation=get_message.get_siteStation(domain)
    cms_finger=get_message.cms_finger(url)
    return None

'''
进行子域名的主动和被动搜集，添加入attack_queue队列
同时对输入域名进行信息搜集，信息存入数据库
最后对attack_queue队列中的页面url深度搜集，进入漏洞扫描
漏洞扫描结果存入数据库
页面按规定显示扫描结果
'''
def Domain_Console(domain):
    max_processes = 3
    attack_queue = multiprocessing.Manager().Queue()
    pool = multiprocessing.Pool(max_processes, init)
    def callback(attack_list):
        for url in attack_list:
            attack_queue.put(url)
    true_domain=domain.split('.',1)[1]
    #主动被动子域名搜集
    pool.apply_async(get_message.GetSubDomain, (true_domain,), callback=callback)
    pool.apply_async(get_message.SubDomainBurst, (true_domain,domain,), callback=callback)
    pool.apply_async(Domain_Message,(true_domain,domain,))
    pool.close()
    pool.join()
    pool.apply_async(SpiderGetUrl.depth_get, (domain,attack_queue,))
    print("end")
    return None

'''
输入格式限制
输入IP格式为:127.0.0.1，输入域名格式为www.baidu.com
域名和IP地址进入不同的模块进行信息搜集
一个进程进入页面深度搜集，页面深度搜集页面会再开四个进程进行attack_url爬取
'''

def Input_Url(url):
    if Domain_IP_Check(url):
        IP_Console(url)
    else:
        Domain_Console(url)

if __name__=='__main__':
    # urls = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    # UrlScan(urls)
    # Input_Url("https://blog.csdn.net/")
    # print(Domain_IP_Check("127.0.0.1"))
    Domain_Console("www.baidu.com")