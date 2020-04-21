import signal
import multiprocessing
import time
import get_message
import re

'''
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

def IP_InQueue(ip):
    return None

def Domain_InQueue(domain):
    return None

#域名和IP地址进入不同的模块进行信息搜集
def Input_Url(url):
    if Domain_IP_Check(url):
        IP_InQueue(url)
    else:
        Domain_InQueue(url)



if __name__=='__main__':
    # urls = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    # UrlScan(urls)
    print(Domain_IP_Check("www.baidu.com"))