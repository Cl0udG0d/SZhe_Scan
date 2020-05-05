from queue import Queue
from lxml import etree
import signal
import multiprocessing
import threading
import time
import core
import urllib3
import ImportToRedis
import redis

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

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



# domain为传入网址网址
def SortOut(urls, domain,redispool):
    new_url_list = []
    for url in urls:
        url = str(url).strip()
        if ("." not in url) and ("javascript:" not in url) and ("#" not in url) and (domain not in url):
            url = domain + url
        if type(url) == list:
            continue
        url = url.strip()
        if not url.startswith("http://") and not url.startswith("https://") and ("javascript:" not in url) and (
                "#" not in url):
            if not domain.endswith("/") and not url.startswith("/"):
                url = domain + "/" + url
            else:
                url = domain + url
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "http://" + url
        if domain not in url:
            continue
        new_url_list.append(url)
    for url in new_url_list:
        print(url)
        redispool.sadd("queue", url)


def Spider(redispool):
    url = redispool.spop("queue")
    new_url_list = []
    try:
        rep = core.gethtml(url, timeout=1)
        rep = etree.HTML(rep)
        url_list = rep.xpath('//*[@href]/@href')
        for new_url in url_list:
            new_url_list.append(new_url)
    except Exception as e:
        print(e)
        pass
    return new_url_list


'''
利用三个列表进行有层次地广度遍历url:all_lists储存所有获取到的url,new_lists储存这一层遍历时获取到的所有新的url，old_lists储存上一层的所有url
用于下层的遍历
'''


class Spyder(threading.Thread):
    def __init__(self, func):
        threading.Thread.__init__(self)
        self.result = self.func()
        self.func = func

    def run(self):
        self.func()

    def get_result(self):
        return self.result


def depth_get(domain,redispool):
    threads = []
    count = 0
    new_url_list = []
    while count < 3:
        count += 1
        print("第%d层" % count + 20 * "=")
        try:
            if count == 1:
                url_list = Spider(redispool)
                new_url_list.extend(url_list)
            else:
                while redispool.scard("queue") != 0:
                    for i in range(1, 26):
                        t = Spyder(Spider)
                        threads.append(t)
                        t.start()
                    for t in threads:
                        t.join()
                        new_url_list.extend(t.get_result())
                    time.sleep(0.5)
        except Exception:
            pass
        SortOut(new_url_list, domain,redispool)
    print("end")
    for url in redispool.smembers("queue"):
        print(url)


if __name__ == '__main__':
    redispool = redis.Redis(connection_pool=ImportToRedis.redisPool)
    redispool.delete("queue")
    redispool.sadd("queue", "https://blog.csdn.net/")
    depth_get("blog.csdn.net",redispool)
