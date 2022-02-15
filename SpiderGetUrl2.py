import re,requests
import time
import core
from Init import redispool

'''
    原来的SpiderGetUrl写的不太好，但还是留在同文件里：SpiderGetUrl.py
    本文件修改自 重剑无锋:https://github.com/TideSec/Common_Spider
    如觉得之前那个文件爬取较好，可以手动修改回去，thanks :)
'''
def url_protocol(url):
    domain = re.findall(r'.*(?=://)', url)
    if domain:
        return domain[0]
    else:
        return url

def same_url(urlprotocol,url):
    url = url.replace(urlprotocol + '://', '')
    if re.findall(r'^www', url) == []:
        sameurl = 'www.' + url
        if sameurl.find('/') != -1:
            sameurl = re.findall(r'(?<=www.).*?(?=/)', sameurl)[0]
        else:
            sameurl = sameurl + '/'
            sameurl = re.findall(r'(?<=www.).*?(?=/)', sameurl)[0]
    else:
        if url.find('/') != -1:
            sameurl = 'www.' + re.findall(r'(?<=www.).*?(?=/)', url)[0]
        else:
            sameurl = url + '/'
            sameurl = 'www.' + re.findall(r'(?<=www.).*?(?=/)', sameurl)[0]
    print('the domain is：' + sameurl)
    return sameurl


class linkQuence:
    def __init__(self):
        self.visited = []    #已访问过的url初始化列表
        self.unvisited = []  #未访问过的url初始化列表
        self.external_url=[] #外部链接

    def getVisitedUrl(self):  #获取已访问过的url
        return self.visited
    def getUnvisitedUrl(self):  #获取未访问过的url
        return self.unvisited
    def getExternal_link(self):
        return self.external_url   #获取外部链接地址
    def addVisitedUrl(self,url):  #添加已访问过的url
        return self.visited.append(url)
    def addUnvisitedUrl(self,url):   #添加未访问过的url
        if url != '' and url not in self.visited and url not in self.unvisited:
            return self.unvisited.insert(0,url)
    def addExternalUrl(self,url):   #添加外部链接列表
        if url!='' and url not in self.external_url:
            return self.external_url.insert(0,url)

    def removeVisited(self,url):
        return self.visited.remove(url)
    def popUnvisitedUrl(self):    #从未访问过的url中取出一个url
        try:                      #pop动作会报错终止操作，所以需要使用try进行异常处理
            return self.unvisited.pop()
        except:
            return None
    def unvisitedUrlEmpty(self):   #判断未访问过列表是不是为空
        return len(self.unvisited) == 0

class Spider():
    '''
    真正的爬取程序
    '''
    def __init__(self,url,domain_url,urlprotocol):
        self.linkQuence = linkQuence()   #引入linkQuence类
        self.linkQuence.addUnvisitedUrl(url)   #并将需要爬取的url添加进linkQuence对列中
        self.current_deepth = 1    #设置爬取的深度
        self.domain_url = domain_url
        self.urlprotocol = urlprotocol

    def getPageLinks(self,url):
        '''
            获取页面中的所有链接
        '''
        try:
            headers = core.GetHeaders()
            content = requests.get(url, timeout=5, headers=headers, verify=False).text.encode('utf-8')
            links = []
            tags = ['a', 'A', 'link', 'script', 'area', 'iframe', 'form']  # img
            tos = ['href', 'src', 'action']
            if url[-1:] == '/':
                url = url[:-1]
            try:
                for tag in tags:
                    for to in tos:
                        link1 = re.findall(r'<%s.*?%s="(.*?)"' % (tag, to), str(content))
                        link2 = re.findall(r'<%s.*?%s=\'(.*?)\'' % (tag, to), str(content))
                        for i in link1:
                            links.append(i)

                        for i in link2:
                            if i not in links:
                                links.append(i)

            except Exception as e:
                print(e)
                print('[!] Get link error')
                pass
            return links
        except:
            return []
    def getPageLinks_bak(self,url):
        '''
        获取页面中的所有链接
        '''
        try:
            headers = core.GetHeaders()
            time.sleep(0.5)
            pageSource = requests.get(url, timeout=5, headers=headers, verify=False).text.encode('utf-8')
            pageLinks = re.findall(r'(?<=href=\").*?(?=\")|(?<=href=\').*?(?=\')', pageSource)
            # print pageLinks
        except:
            # print ('open url error')
            return []
        return pageLinks

    def processUrl(self,url):
        '''
        判断正确的链接及处理相对路径为正确的完整url
        :return:
        '''
        true_url = []
        in_link = []
        excludeext = ['.zip', '.rar', '.pdf', '.doc', '.xls', '.jpg', '.mp3', '.mp4','.png', '.ico', '.gif','.svg', '.jpeg','.mpg', '.wmv', '.wma','mailto','javascript','data:image']
        for suburl in self.getPageLinks(url):
            exit_flag = 0
            for ext in excludeext:
                if ext in suburl:
                    print("break:" + suburl)
                    exit_flag = 1
                    break
            if exit_flag == 0:
                if re.findall(r'/', suburl):
                    if re.findall(r':', suburl):
                        true_url.append(suburl)
                    else:
                        true_url.append(self.urlprotocol + '://' + self.domain_url + '/' + suburl)
                else:
                    true_url.append(self.urlprotocol + '://' + self.domain_url + '/' + suburl)

        for suburl in true_url:
            print('from:' + url + ' get suburl：' + suburl)

        return true_url

    def sameTargetUrl(self,url):
        same_target_url = []
        for suburl in self.processUrl(url):
            if re.findall(self.domain_url,suburl):
                same_target_url.append(suburl)
            else:
                self.linkQuence.addExternalUrl(suburl)
        return same_target_url

    def unrepectUrl(self,url):
        '''
        删除重复url
        '''
        unrepect_url = []
        for suburl in self.sameTargetUrl(url):
            if suburl not in unrepect_url:
                unrepect_url.append(suburl)
        return unrepect_url

    def crawler(self,crawl_deepth=1):
        '''
        正式的爬取，并依据深度进行爬取层级控制
        '''
        self.current_deepth=0
        print("current_deepth:", self.current_deepth)
        while self.current_deepth < crawl_deepth:
            if self.linkQuence.unvisitedUrlEmpty():break
            links=[]
            while not self.linkQuence.unvisitedUrlEmpty():
                visitedUrl = self.linkQuence.popUnvisitedUrl()
                if visitedUrl is None or visitedUrl == '':
                    continue
                print("#"*30 + visitedUrl +" :begin"+"#"*30)
                for sublurl in self.unrepectUrl(visitedUrl):
                    links.append(sublurl)
                # links = self.unrepectUrl(visitedUrl)
                self.linkQuence.addVisitedUrl(visitedUrl)
                print("#"*30 + visitedUrl +" :end"+"#"*30 +'\n')
            for link in links:
                self.linkQuence.addUnvisitedUrl(link)
            self.current_deepth += 1
        # print(self.linkQuence.visited)
        # print (self.linkQuence.unvisited)
        urllist=[]
        urllist.append("#" * 30 + ' VisitedUrl ' + "#" * 30)
        for suburl in self.linkQuence.getVisitedUrl():
            urllist.append(suburl)
        urllist.append('\n'+"#" * 30 + ' UnVisitedUrl ' + "#" * 30)
        for suburl in self.linkQuence.getUnvisitedUrl():
            urllist.append(suburl)
        urllist.append('\n'+"#" * 30 + ' External_link ' + "#" * 30)
        for sublurl in self.linkQuence.getExternal_link():
            urllist.append(sublurl)
        urllist.append('\n'+"#" * 30 + ' Active_link ' + "#" * 30)
        actives = ['?', '.asp', '.jsp', '.php', '.aspx', '.do', '.action']
        active_urls = []
        for sublurl in urllist:
            for active in actives:
                if active in sublurl:
                    active_urls.append(sublurl)
                    break
        for active_url in active_urls:
            urllist.append(active_url)
        return urllist

def writelog(domain,urllist):
    # filename=log
    # outfile=open(filename,'w')
    # for suburl in urllist:
    #     outfile.write(suburl+'\n')
    # outfile.close()
    for url in urllist:
        redispool.sadd(domain, url)

def SpiderGetUrl2(url,deepth=2):
    try:
        craw_deepth=int(deepth)
        urlprotocol = url_protocol(url)
        domain_url = same_url(urlprotocol, url)
        print("domain_url:" + domain_url)
        spider = Spider(url, domain_url, urlprotocol)
        urllist = spider.crawler(craw_deepth)
        writelog(domain_url, urllist)
        print('-' * 20 + url + '-' * 20)
        for sublurl in urllist:
            print(sublurl)
        print("Spider Url Length is :" + str(len(urllist)))
        print('\n' + 'SpiderGetUrl End ! ' + domain_url)
    except:
        pass
if __name__ == '__main__':
    SpiderGetUrl2('https://www.cnblogs.com/Cl0ud/',1)