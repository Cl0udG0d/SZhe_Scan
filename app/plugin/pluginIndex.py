#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/3/6 12:12
# @Author  : Cl0udG0d
# @File    : pluginIndex.py
# @Github: https://github.com/Cl0udG0d
import os

class Platform:
    def __init__(self,urllist,position):
        self.urllist=urllist
        self.position=position
        self.allPlugins=self.loadPlugins()
        self.runAllUrl()

    def loadPlugins(self):
        '''
        加载插件
        '''
        currdir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "../plugins/")
        allPlugins=[]
        for filename in os.listdir(currdir):
            if not filename.endswith(".py") or filename.startswith("_"):
                continue
            allPlugins.append(filename)
        return allPlugins

    def runPlugin(self, filename,url):
        '''
        运行插件
        '''
        pluginName=os.path.splitext(filename)[0]
        plugin=__import__("plugins."+pluginName,fromlist=[pluginName])
        #Errors may be occured. Handle it yourself.
        plugin.run(url)

    def runAllUrl(self):
        for url in self.urllist:
            for plugin in self.allPlugins:
                self.runPlugin(plugin,url)
        return


def test():
    print('hi')


if __name__ == '__main__':
    platform=Platform()
