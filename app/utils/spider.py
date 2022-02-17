#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18/4/14 上午2:07
# @Author  : SecPlus
# @Site    : www.SecPlus.org
# @Email   : TideSecPlus@gmail.com

# 2018.04.14 结合wdscan和其他爬虫，相对比较完善的spider

import random
import re,requests
import time
import logging
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from app.utils.randomAgent import getRandomUserAgent

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def url_protocol(url):
    domain = re.findall(r'.*(?=://)', url)
    if domain:
        return domain[0]
    else:
        return 'http'

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
    exts_pattern=re.compile("([a-zA-Z0-9\-\/._~%!$&'()*+]+)?")
    if '/' in url and len(url.split('/'))>1:
        exts='/'.join(url.split('/')[:-1])
        return exts
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
            headers = getRandomUserAgent()
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
                logging.warning(e)
                logging.warning('[!] Get link error')
                pass
            return links
        except:
            return []
    def getPageLinks_bak(self,url):
        '''
        获取页面中的所有链接
        '''
        try:

            # pageSource=urllib2.urlopen(url).read()
            headers = getRandomUserAgent()
            time.sleep(0.5)
            pageSource = requests.get(url, timeout=5, headers=headers).text.encode('utf-8')
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
        filter_exts=[]
        for suburl in self.getPageLinks(url):


            if re.findall(r'/', suburl):
                if re.findall(r':', suburl):
                    true_url.append(suburl)
                else:
                    true_url.append(self.urlprotocol + '://' + self.domain_url + '/' + suburl)
            else:
                true_url.append(self.urlprotocol + '://' + self.domain_url + '/' + suburl)

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
        logging.info("current_deepth:", self.current_deepth)
        while self.current_deepth < crawl_deepth:
            if self.linkQuence.unvisitedUrlEmpty():break
            links=[]
            while not self.linkQuence.unvisitedUrlEmpty():
                visitedUrl = self.linkQuence.popUnvisitedUrl()
                if visitedUrl is None or visitedUrl == '':
                    continue
                for sublurl in self.unrepectUrl(visitedUrl):
                    links.append(sublurl)
                # links = self.unrepectUrl(visitedUrl)
                self.linkQuence.addVisitedUrl(visitedUrl)
            for link in links:
                self.linkQuence.addUnvisitedUrl(link)
            self.current_deepth += 1
        # print(self.linkQuence.visited)
        # print (self.linkQuence.unvisited)
        urllist=[]
        # urllist.append("#" * 30 + ' VisitedUrl ' + "#" * 30)
        for suburl in self.linkQuence.getVisitedUrl():
            urllist.append(suburl)
        # urllist.append('\n'+"#" * 30 + ' UnVisitedUrl ' + "#" * 30)
        for suburl in self.linkQuence.getUnvisitedUrl():
            urllist.append(suburl)
        for sublurl in self.linkQuence.getExternal_link():
            urllist.append(sublurl)
        active_urls=self.filter(urllist)

        for active_url in active_urls:
            urllist.append(active_url)
        return active_urls

    def filter(self,urllist):
        active_urls=[]
        actives = ['?', '.asp', '.jsp', '.php', '.aspx', '.do', '.action']
        filter_pattern = re.compile('/\w+.*\.(css|png|gif|jpg|jpeg|swf|tiff|pdf|ico|flv|mp4|mp3|avi|mpg|gz|mpeg|iso|dat|rar|mov|exe|tar|zip|bin|bz2|xsl|'
        'doc|docx|ppt|pptx|xls|xlsx|csv|map|ttf|tif|woff|woff2|cab|apk'
        '|bmp|svg|exif|xml|rss|webp|js|html)\?')
        allown_pattern=re.compile('/\w+\.(asp|jsp|php|aspx|do|action)')
        query_pattern=re.compile('\?[a-zA-Z0-9&=;%!@#$^()\[\]\{\}\'\":,.]+')
        query_set=set()
        for sublurl in urllist:
            subdomain=sublurl.lstrip('http://') if sublurl.startswith('http://') else sublurl
            subdomain=subdomain.lstrip('https://') if subdomain.startswith('https://') else subdomain

            if subdomain.startswith(self.domain_url) and len(subdomain.split(self.domain_url))==2:
                query_curr = query_pattern.findall(sublurl)

                if sublurl.endswith('/') or allown_pattern.findall(sublurl):
                    if '?' in sublurl:
                        if query_curr and query_curr[0][:10] not in query_set:
                            query_set.add(query_curr[0][:10])
                            active_urls.append(sublurl)
                    elif sublurl.endswith('//'):
                        pass
                    else:
                        active_urls.append(sublurl)
                else:

                    if not filter_pattern.findall(sublurl):
                        query_curr = query_pattern.findall(sublurl)
                        if query_curr and query_curr[0][:10] not in query_set:
                            query_set.add(query_curr[0][:10])
                            active_urls.append(sublurl)
                    elif allown_pattern.findall(sublurl):
                        active_urls.append(sublurl)

        return active_urls


def writelog(log,urllist):
    filename=log
    outfile=open(filename,'w')
    for suburl in urllist:
        outfile.write(suburl+'\n')
    outfile.close()


def spider(url,craw_deepth =1):
    try:
        urlprotocol = url_protocol(url)  # 获取协议
        domain_url = same_url(urlprotocol, url)
        logging.info("domain_url:" + domain_url)
        spider = Spider(url, domain_url, urlprotocol)
        urllist = spider.crawler(craw_deepth)
        return urllist
    except Exception as e:
        logging.warning(e)
        return []


if __name__ == '__main__':
    url = 'http://www.powermos.com/index.php?m=Index&a=index'
    result=spider(url,craw_deepth =1)
    print("spider end,result length is {}".format(len(result)))

