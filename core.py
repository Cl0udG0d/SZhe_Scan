from changanya.simhash import Simhash
import requests
from init import redispool
import random


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF', 'jpeg'])

def GetTargetCount():
    count = redispool.hget('targetscan', 'waitcount')
    if 'str' in str(type(count)):
        waitcount=int(redispool.hget('targetscan', 'waitcount'))
    else:
        waitcount=0
    target={
        "sumcount":redispool.pfcount("domain")+redispool.pfcount("ip"),
        "waitcount":waitcount,
        "nowscan":redispool.hget("targetscan", "nowscan")
    }
    return target

def GetServices():
    service={
        "http":redispool.pfcount("http"),
        "ssh":redispool.pfcount("ssh"),
        "mysql":redispool.pfcount("mysql"),
        "http_proxy":redispool.pfcount("http-proxy"),
        "mongodb":redispool.pfcount("mongodb"),
        "ftp":redispool.pfcount("ftp"),
        "tcpwrapped":redispool.pfcount("tcpwrapped"),
        "http_alt":redispool.pfcount("http-alt"),
        "telnet":redispool.pfcount("telnet"),
        "https":redispool.pfcount("https"),
        "redis":redispool.pfcount("redis")
    }
    return service

def GetPort():
    ports={
        "test80":redispool.pfcount("test80"),
        "test8080":redispool.pfcount("test8080"),
        "test443":redispool.pfcount("test443"),
        "test8081":redispool.pfcount("test8081"),
        "test22":redispool.pfcount("test22"),
        "test85":redispool.pfcount("test85"),
        "test3389":redispool.pfcount("test3389"),
        "test9000":redispool.pfcount("test9000"),
        "test8088":redispool.pfcount("test8088"),
        "test8090":redispool.pfcount("test8090"),
        "test3306":redispool.pfcount("test3306"),
        "test8000": redispool.pfcount("test8000")
    }
    return ports

def GetCounts():
    counts={
        "domaincount":redispool.pfcount("domain"),
        "ipcount":redispool.pfcount("ip"),
        "bugcount":redispool.pfcount('serious')+redispool.pfcount('High')+redispool.pfcount('medium')+redispool.pfcount('low'),
        "poccount":redispool.pfcount("poc"),
        "havebugpc":redispool.pfcount("havebugpc"),
        "seriouscount":redispool.pfcount('Serious'),
        "sencount":redispool.pfcount("SenDir")
    }
    return counts

def GetBit():
    '''
    操作redis HyperLogLog进行计数
    :return:
    '''
    seriouscount = redispool.pfcount('Serious')
    highcount =  redispool.pfcount('High')
    mediumcount =  redispool.pfcount('Medium')
    lowcount =  redispool.pfcount('Low')
    allcount=seriouscount+highcount+mediumcount+lowcount
    sqlcount= redispool.pfcount('SQLBugScan')
    comincount= redispool.pfcount('ComInScan')
    weblogiccount= redispool.pfcount('WebLogicScan')
    fileincount= redispool.pfcount('FileIncludeScan')
    sendircount= redispool.pfcount('SenDir')
    robotscount= redispool.pfcount('robots文件发现')
    phpinfocount= redispool.pfcount('phpstudy探针')
    gitcount= redispool.pfcount('git源码泄露扫描')
    phpstudycount= redispool.pfcount('phpstudy phpmyadmin默认密码漏洞')
    otherpoc=allcount-sqlcount-comincount-weblogiccount-fileincount-sendircount-robotscount-phpinfocount-gitcount
    bugbit={
        'seriouscount':seriouscount,
        'highcount':highcount,
        'mediumcount':mediumcount,
        'lowcount':lowcount,
        'allcount': allcount,
    }
    if allcount==0:
        bugtype = {
            'SQLBugScan': 0,
            'ComInScan': 0,
            'WebLogicScan': 0,
            'FileIncludeScan': 0,
            'SenDir': 0,
            'robots文件发现': 0,
            'phpstudy探针': 0,
            'git源码泄露扫描': 0,
            'phpstudy phpmyadmin默认密码漏洞': 0,
            'POC扫描漏洞': 0
        }
    else:
        bugtype={
            'SQLBugScan':sqlcount/allcount*100,
            'ComInScan':comincount/allcount*100,
            'WebLogicScan':weblogiccount/allcount*100,
            'FileIncludeScan':fileincount/allcount*100,
            'SenDir':sendircount/allcount*100,
            'robots文件发现':robotscount/allcount*100,
            'phpstudy探针':phpinfocount/allcount*100,
            'git源码泄露扫描':gitcount/allcount*100,
            'phpstudy phpmyadmin默认密码漏洞':phpstudycount/allcount*100,
            'POC扫描漏洞':otherpoc/allcount*100
        }
    return bugbit,bugtype

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


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# def get_newname(filename):
#     return "head."+filename.rsplit('.', 1)[1]


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
