from sqlinjection import ErrorInjection,BoolInjection,TimeInjection
import urllib.parse as urlparse
import core

'''
传入url为http://www.xxx.com格式，或者是www.xxx.com 可带参数如www.xxx.com/index.php?id=1
检测三种注入：
    1，报错注入
    2，布尔注入
    3，时间注入
每种注入有相应的payload进行检测，在payload检测之前进行waf的探测，即check_waf.py
三个注入检测函数传入检测url和正常访问时的html代码，加入payload之后通过计算页面相似度来判断是否遇到了waf
'''
def InjectionControl(url):
    old_html=core.gethtml(url)
    domain = url.split("?")[0]
    #获取域名和参数，用来构建payload
    queries = urlparse.urlparse(url).query.split("&")
    if old_html and any(queries):
        e_vulnerable, e_db,e_payload =ErrorInjection.ErrorIn(domain, queries, old_html)
        if e_vulnerable:
            return True,e_db,e_payload
        t_vulnerable, t_db,t_payload =TimeInjection.TimeIn(domain, queries, old_html)
        if t_vulnerable:
            return True,t_db,t_payload
        b_vulnerable, b_db ,b_payload=BoolInjection.BoolIn(domain, queries, old_html)
        if b_vulnerable:
            return True,b_db,b_payload
        if e_db:
            return False,"waf"
        else:
            return False,None
    else:
        return False, None

if __name__=='__main__':
    # injection_control("http://testphp.vulnweb.com:80/listproducts.php?cat=1")
    # injection_control("http://www.sh-redflag.com/en/Newshow.asp?byID=38")
    # injection_control("http://www.iiaiia.org/NewShow.asp?byID=1416")
    # injection_control("http://hfdjc.cn/NewShow.asp?byID=1037")
    print(InjectionControl("http://testphp.vulnweb.com/listproducts.php?cat=1"))
    print(InjectionControl("http://www.yuebooemt.com/about.php?id=37"))


