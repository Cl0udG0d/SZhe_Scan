from changanya.simhash import Simhash
import requests
from init import redispool
import random


def GetHeaders():
    index=random.randint(0, redispool.llen('useragents'))
    useragent = redispool.lindex('useragents',index)
    return {'User-Agent': useragent}


def gethtml(url, timeout=2):
    if not (url.startswith("http://") or url.startswith("https://")):
        url = "http://" + url
    try:
        rep = requests.get(url, headers=GetHeaders(), timeout=timeout, verify=False)
        html = rep.text
    except Exception as e:
        # 不管其返回的是错误，null，都将其页面放入html，留给check_waf计算相似度
        html = str(e)
        pass
    return html


def wordlistimport(file):
    payloadlist = []
    try:
        with open(file, 'r') as f:
            for line in f:
                final = str(line.replace("\n", ""))
                payloadlist.append(final)
        return payloadlist
    except Exception as e:
        print(e)
        pass


def is_similar_page(res1, res2, radio):
    '''
    计算页面相似度函数
    '''
    if res1 is None or res2 is None:
        return False
    # body1 = res1.text
    # body2 = res2.text

    simhash1 = Simhash(str(res1))
    simhash2 = Simhash(str(res2))

    calc_radio = simhash1.similarity(simhash2)
    if calc_radio >= float(radio):
        return True
    else:
        return False


'''
if 响应码 == 404:
    return this_is_404_page
elif 目标网页内容 与 网站404页面内容 相似：
    return this_is_404_page
else:
    return this_is_not_404_page
'''


def is_404(true_404_html, check_url_html):
    '''
    检测页面是否为404
        1,从状态码是否为404判断
        2,获取域名的404页面，然后判断请求的页面和404页面是否相似，相似则可以判断为404页面。
    当check_url为404页面时，返回true，否则返回false
    传入的参数为(真实的404界面，需要检测的url)，是能直接访问的url，形如http://xxx/xxx.html 非域名
    参考链接：
        https://xz.aliyun.com/t/4404
        https://thief.one/2018/04/12/1/
    :return:
    '''
    if true_404_html.status_code == 404:
        return True
    else:
        if is_similar_page(true_404_html.text, check_url_html.text, radio=0.85):
            return True
        else:
            return False


# 测试数据
# print(is_404("https://www.baidu.com/search/error.html","https://www.baidu.com/xxxxxxxxxxxxxxxxxxxxxxxxxxxx"))

if __name__ == '__main__':
    # html = gethtml("http://testphp.vulnweb.com:80/listproducts.php?cat=1'")
    # print(html)
    for i in range(1000):
        print(GetHeaders())
