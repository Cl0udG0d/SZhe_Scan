import signal
import multiprocessing

'''
====进程是资源分配的单位，线程是操作系统调度的单位====
获取target目标url，进行同域名下的及网页中的输入源搜集
输入形式都可，进行自主判断
               创建进程池，多进程进行扫描，实现并行效果，配置文件config.py
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

def index(url):

def scan(urls):
    results={}
    max_processes = 10
    pool = multiprocessing.Pool(max_processes, init)
    #将输入urls列表遍历放入进程池中，扫描结果放入results字典中
    for url in urls:
        def callback(result,url=url):
            results[url] = result
        pool.apply_async(index, (url,), callback=callback)
