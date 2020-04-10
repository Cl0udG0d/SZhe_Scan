#-*- coding:utf-8 -*-

import requests
from lxml import etree
import time

headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6) ",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "en-us",
           "Connection": "keep-alive",
           "Accept-Charset": "GB2312,utf-8;q=0.7,*;q=0.7"}

def get_recordinfo(domain):
    '''
    返回域名的备案信息
    :param domain:
    :return:
    '''
    check_url = 'http://www.beianbeian.com/s-0/'+domain+'.html'
    rep = requests.get(check_url, headers=headers)
    rep = etree.HTML(rep.text)
    thead = rep.xpath('//table[@class="layui-table res_table"]//th/text()')
    td_4 = "".join(rep.xpath('//tbody[@id="table_tr"]//td[4]/a/text()'))
    td_6 = " ".join(rep.xpath('//tbody[@id="table_tr"]//td[6]/a/text()'))
    td_8 = "".join(rep.xpath('//tbody[@id="table_tr"]//td[8]/a/text()'))
    tbody = rep.xpath('//tbody[@id="table_tr"]//td[1]/text()')
    tbody.append("".join(rep.xpath('//tbody[@id="table_tr"]//td[2]/text()')))
    tbody.append("".join(rep.xpath('//tbody[@id="table_tr"]//td[3]/text()')))
    tbody.append(td_4)
    tbody.append("".join(rep.xpath('//tbody[@id="table_tr"]//td[5]/text()')))
    tbody.append(td_6)
    tbody.append("".join(rep.xpath('//tbody[@id="table_tr"]//td[7]/text()')))
    tbody.append(td_8)
    #context2[3] = context3[0]+context3[1]
    #context2[4] = homeURL
    for i in zip(thead,tbody):
            print(":".join(i))

    


def get_ip(domain):
    '''
    返回域名的历史解析记录字符串
    :param domain:
    :return:
    '''

    ip138_url = 'https://site.ip138.com/' + domain
    rep = requests.get(ip138_url, headers=headers)
    rep = etree.HTML(rep.text)
    context = rep.xpath('//div[@id="J_ip_history"]//a/text()')
    str = "\n".join(context)
    print(str)


def get_siteStation(ip):
    '''

    '''
    data ={'domain':ip}
    url_1='https://www.webscan.cc/search/'
    rep1 = requests.post(url_1, data=data, headers=headers)
    rep1 = etree.HTML(rep1.text)
    text1 = rep1.xpath('//a[@class="domain"]/text()')
    url_2_base='http://stool.chinaz.com'
    url_2='http://stool.chinaz.com/same?s='+ip+'&page=1'
    text2=[]
    while(1):
        rep2 = requests.get(url_2,headers=headers)
        rep2 = etree.HTML(rep2.text)
        new_list= rep2.xpath('//div[@class="w30-0 overhid"]/a/text()')
        if(len(new_list)==0):
            break
        text2+=new_list
        next_url = "".join(rep2.xpath('//a[@title="下一页"]/@href'))
        url_2 = url_2_base+next_url
    url_3='http://www.114best.com/ip/114.aspx?w='+ip
    rep3 = requests.get(url_3,headers=headers)
    rep3 = etree.HTML(rep3.text)
    text3 = rep3.xpath('//div[@id="rl"]/span/text()')
    text3 = [x.strip() for x in text3]
    text=list(set(text1).union(set(text2)).union(set(text3)))
    for i in text:
        if "屏蔽的关键字" in i:
            text.remove(i)
    str = "\n".join(text)
    return str


def Subdomain_burst(domain,filename):
    file = open(r"dict\SUB_scan.txt","r")
    resultFile = open(filename,"a+")
    for line in file.readlines():
        url = 'http://'+line.replace("\n",'.'+domain)
        r = requests.get(url,headers = headers)
        if r.status_code==200:
            resultFile.write(url+"\n")


def sensitive_scan(domain,filename):
    file = open(r"dict\SEN_scan.txt","r",encoding='utf-8')
    resultFile = open(filename,"a+")
    for line in file.readlines():
        url = 'http://'+domain+line.replace("\n",'')
        r = requests.get(url,headers = headers,allow_redirects=False)
        if r.status_code==200:
            resultFile.write(url+"\n")



if __name__ == '__main__':
        #get_recordinfo("baidu.com")
        #get_ip("google.com")
        #get_siteStation("172.217.27.142")
    Subdomain_burst("baidu.com","dict\test1.txt")
    sensitive_scan("www.anantest.com",dict\test2.txt)
    #hhh(r"dict\result\test2.txt")
