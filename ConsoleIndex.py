import time
import re
import signal
import multiprocessing
import redis
from BaseMessage import GetBaseMessage
from IPMessage import IPMessage
from DomainMessage import DomainMessage

'''
ip和域名进入不同的调度函数扫描
====进程是资源分配的单位，线程是操作系统调度的单位====
'''

def init():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

#当为ip地址时返回true，否则认为是域名
def Domain_IP_Check(url):
    pattern = re.compile('^\d+\.\d+\.\d+\.\d+$')
    if pattern.findall(url):
        return True
    else:
        return False

def UrlScan(urls):
    vulnerables = [] #存储有漏洞的url
    results = {} #存储扫描结果
    max_processes = 8
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


def BaseConsole(url,redispool):
    GetBaseMessage(url,redispool)

def IP_Console(ip,redispool):
    IPMessage(ip,redispool)

def Domain_Console(domain,redispool):
    DomainMessage(domain,redispool)

'''
输入格式限制
输入IP格式为:127.0.0.1，输入域名格式为www.baidu.com
域名和IP地址进入不同的模块进行信息搜集
一个进程进入页面深度搜集，页面深度搜集页面会再开四个进程进行attack_url爬取
'''

def ConsoleUrl(urls):
    redispool=redis.ConnectionPool(host='127.0.0.1',port=6379, decode_responses=True)
    max_processes = 8
    pool = multiprocessing.Pool(max_processes, init)
    for url in urls:
        pool.apply_async(BaseConsole, (url,redispool,))
        if Domain_IP_Check(url):
            pool.apply_async(IP_Console, (url,redispool,))
        else:
            pool.apply_async(Domain_Console, (url,redispool,))
    pool.close()
    pool.join()


if __name__=='__main__':
    ConsoleUrl("www.baidu.com")
