#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/3/17 0:40
# @Author  : Cl0udG0d
# @File    : szheException.py
# @Github: https://github.com/Cl0udG0d


class reqBadExceptin(Exception):
    "this is user's Exception for check the length of name "
    def __init__(self,url):
        self.url = url
    def __str__(self):
        return "请求失败 {}".format(self.url)


def test():
    print('hi')


if __name__ == '__main__':
    test()
