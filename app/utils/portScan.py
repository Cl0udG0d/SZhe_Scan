#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/2/16 17:17
# @Author  : Cl0udG0d
# @File    : portScan.py
# @Github: https://github.com/Cl0udG0d
'''
    NMap(Network Mapper)
    调用nmap进行端口扫描，传入主机IP，实例化一个扫描对象nm
    获取所有扫描协议的列表，输出所有协议扫描的开放端口以及相应端口对应的服务
    设置扫描参数: -Pn -sV --open -T3 -n --host-timeout=60s --min-rate=500
'''


def PortScan(host):
    pattern = re.compile('^\d+\.\d+\.\d+\.\d+(:(\d+))?$')
    content = ""
    if not pattern.findall(host):
        host = socket.gethostbyname(host)
    if pattern.findall(host) and ":" in host:
        host=host.split(":")[0]
    nm = nmap.PortScanner()
    try:
        nm.scan(host, arguments='-Pn -sV --open -T3 -n --host-timeout=60s --min-rate=500')
        for proto in nm[host].all_protocols():
            lport = list(nm[host][proto].keys())
            for port in lport:
                if nm[host][proto][port]['state'] == "open":
                    service = nm[host][proto][port]['product']
                    version = nm[host][proto][port]['version']
                    content += '[*]主机' + host + ' 协议：' + proto + '\t开放端口号：' + str(port) + '\t端口服务：' + service + '\t版本：' + version + "\n"
        return content
    except Exception as e:
        nmap.sys.exit(0)

def test():
    print('hi')


if __name__ == '__main__':
    test()
