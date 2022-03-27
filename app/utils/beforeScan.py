#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/3/26 23:27
# @Author  : Cl0udG0d
# @File    : beforeScan.py
# @Github: https://github.com/Cl0udG0d
import importlib
import os
import re
import logging
from pip._internal import main
import sys

def getPluginDepends():
    pattern = re.compile("^import (.*?)$")
    moduleKeys=list(sys.modules.keys())
    currdir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "../plugins/")
    for files in os.listdir(currdir):
        if os.path.splitext(files)[1] == '.py' and not files.startswith("_"):
            filename = os.path.splitext(files)[0]
            filepath=currdir+"/"+filename+".py"
            logging.info("{} is Checking".format(filepath))
            with open(filepath, 'r') as f:
                for line in f.readlines():
                    result=pattern.findall(line.strip())
                    if result:
                        name=result[0]
                        if name and checkLib(name,moduleKeys):
                            logging.info("{} Lib is Loading".format(name))
                            install(name)
                        else:
                            print("{} Lib is Loaded".format(name))
    return


def install(package,source="https://pypi.tuna.tsinghua.edu.cn/simple"):
    main(['install', package,'-i',source])


def checkLib(libName,moduleKeys):
    try:
        if libName in moduleKeys:
            return False
        importlib.import_module(libName)
        return False
    except Exception as e:
        logging.warning(e)
        return True


def test():
    name="import re dd"
    pattern=re.compile("^import (.*?)$")
    print(pattern.findall(name))


if __name__ == '__main__':
    getDepends("../plugins")
