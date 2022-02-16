#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/2/16 16:23
# @Author  : Cl0udG0d
# @File    : core.py
# @Github: https://github.com/Cl0udG0d
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



def test():
    print('hi')


if __name__ == '__main__':
    test()
