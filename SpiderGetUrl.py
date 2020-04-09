import requests
from lxml import etree
from fake_useragent import UserAgent
import queue
ua = UserAgent()



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
def spider(url):
    headers = {'User-Agent': ua.random}
    new_url_list = []
    try:
        rep = requests.get(url,headers=headers,timeout=1.5)
        rep = etree.HTML(rep.text)
        url_list = rep.xpath('//*[@href]/@href')

        for i in url_list:
            if "http" in i:
                new_url_list.append(i)
            else:
                new_url_list.append(url + i)
    except:
        pass

    return new_url_list
'''
利用三个列表进行有层次地广度遍历url:all_lists储存所有获取到的url,new_lists储存这一层遍历时获取到的所有新的url，old_lists储存上一层的所有url
用于下层的遍历
'''
def depth_get(url):
    count=0
    all_lists=[]
    new_lists=[]
    new_lists.append(url)
    while(count<2):
        count+=1
        print("第%d层"%count+20*"=")
        old_lists=new_lists
        new_lists=[]
        for node in old_lists:
            new_lists+=spider(node)
        all_lists+=new_lists
    all_lists = list(set(all_lists))
    # for i in all_lists:
    #     print(i)
    return all_lists

#测试数据
#depth_get("https://ask.hellobi.com/blog/bixtcexs/11983")