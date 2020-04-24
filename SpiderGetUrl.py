from lxml import etree
import signal
import multiprocessing
import time
import core

'''
因为每深入一层，链接数增大很多，所以截止层数暂定为2，添加多线程之后将层数提高
爬取截止条件为：层数为2，或者队列中无新的链接
返回链接列表
参考链接:
    https://www.hss5.com/2018/11/28/python%E7%88%AC%E5%8F%96%E7%BD%91%E7%AB%99%E5%85%A8%E9%83%A8url%E9%93%BE%E6%8E%A5/
    https://ask.hellobi.com/blog/bixtcexs/11983
    https://lskreno.vip/2019/09/15/%E7%88%AC%E8%99%AB%E4%B9%8B%E6%88%98/
    https://github.com/sml2h3/python_collect_domain/blob/master/collect.py
'''


def init():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

#domain为传入网址网址
def SortOut(urls,domain,queue):
    new_url_list=[]
    for url in urls:
        url=url.strip()
        if ("." not in url) and ("javascript:;" not in url) and ("#" not in url):
            url=domain+url
        elif domain not in url:
            continue
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        new_url_list.append(url)
    new_url_list = list(set(new_url_list))
    for url in new_url_list:
        print(url)
        queue.put(url)


def Spider(queue):
    url=queue.get()
    new_url_list=[]
    try:
        rep = core.gethtml(url)
        rep = etree.HTML(rep)
        url_list = rep.xpath('//*[@href]/@href')
        for new_url in url_list:
            new_url_list.append(new_url)
    except Exception as e:
        print(e)
        pass
    return new_url_list

# def normal(url):
#     count=0
#     start=datetime.datetime.now()
#     urls=[]
#     urls.append(url)
#     while (count < 2):
#         new_url_list=[]
#         count+=1
#         print("第%d层"%count+20*"=")
#         try:
#             for url in urls:
#                 rep = core.gethtml(url, timeout=1)
#                 rep = etree.HTML(rep)
#                 url_list = rep.xpath('//*[@href]/@href')
#                 for new_url in url_list:
#                     if new_url != "javascript:;" and new_url != "#":
#                         if not (new_url.startswith("http://") or new_url.startswith("https://")):
#                             new_url = "http://" + new_url
#                         new_url_list.append(new_url)
#         except Exception as e:
#             print(e)
#             pass
#         new_url_list=list(set(new_url_list))
#         urls=new_url_list
#     print("end")
#     end=datetime.datetime.now()
#     print(end-start)
'''
利用三个列表进行有层次地广度遍历url:all_lists储存所有获取到的url,new_lists储存这一层遍历时获取到的所有新的url，old_lists储存上一层的所有url
用于下层的遍历
'''

def depth_get(domain,attck_queue):
    #最大进程数为4
    max_processes = 4
    pool = multiprocessing.Pool(max_processes, init)
    count=0
    # start=datetime.datetime.now()
    def callback(url_list):
        new_url_list.extend(url_list)
    while (count < 2):
        new_url_list=[]
        count+=1
        print("第%d层"%count+20*"=")
        try:
            if count==1:
                url_list=Spider(attack_queue)
                new_url_list.extend(url_list)
            else:
                while not attck_queue.empty():
                    pool.apply_async(Spider, (attck_queue,), callback=callback)
                    pool.apply_async(Spider, (attck_queue,), callback=callback)
                    pool.apply_async(Spider, (attck_queue,), callback=callback)
                    pool.apply_async(Spider, (attck_queue,), callback=callback)
                    time.sleep(0.5)
        except Exception:
            pass
        SortOut(new_url_list,domain,attck_queue)
    pool.close()
    pool.join()
    print("end")
    return attack_queue
    # return attck_queue
    # end=datetime.datetime.now()
    # print(end-start)


'''
测试数据
    depth_get函数是广度遍历爬取url控制函数
    SortOut是去重和整理冗余无用url函数
    Spider是爬取页面的函数
    normal是没有使用多进程的普通爬取函数
    相比较于普通函数，多进程函数多了整理冗余数据和错误url的功能，对于网站：https://blog.csdn.net/
    深度二重爬取url时间：（使用datetime.datetime.now()进行计算）
        depth_get函数：0:00:28.969321
        normal函数：0:00:01.031345
'''
if __name__=='__main__':
    attack_queue = multiprocessing.Manager().Queue()
    attack_queue.put("http://www.dedecms.com/")
    depth_get("www.dedecms.com",attack_queue)
    # normal("https://blog.csdn.net/")