
'''
    简易版漏洞检测框架
'''

import os
import time
import importlib
# m=importlib.import_module('m1.t')
# m.test1()
# m._test2()

def banner(config):
    msg = '''{}'''.format(config['VERSION'])
    print(msg)



def init(config: dict):
    print("[*] target:{}".format(config["url"]))
    pocList=[]
    # 加载poc，首先遍历出路径
    _pocs = []
    for root, dirs, files in os.walk(config['PATHS_POCS']):
        for x in files:
            modelName=x.split('.')[0]
            m = importlib.import_module("pocs."+modelName)
            pocList.append(m)
    return pocList

def end():
    print("[*] shutting down at {0}".format(time.strftime("%X")))


def start(config: dict,pocList):
    url_list = config.get("url", [])
    # 循环url_list与pocs，逐一对应执行。
    for i in url_list:
        for poc in pocList:
            try:
                ret = poc._verify(i)
            except Exception as e:
                ret = None
                print(e)
            if ret:
                print("漏洞存在")
                print(ret)


def main():
    PATHS_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)))
    PATHS_POCS = os.path.join(PATHS_ROOT, "pocs")
    # print(PATHS_POCS)
    # print(PATHS_ROOT)
    config = {
        "VERSION":0.01,
        "url": ["http://223.68.174.194:8888", "http://157.0.142.246:10000"],
        "poc": [],
        'PATHS_POCS':PATHS_POCS,
        'PATHS_ROOT':PATHS_ROOT
    }
    banner(config)
    pocList=init(config)
    start(config,pocList)
    end()


if __name__ == '__main__':
    main()