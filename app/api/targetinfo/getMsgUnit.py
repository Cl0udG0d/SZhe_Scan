import re
import nmap
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


'''
NMap(Network Mapper)
调用nmap进行端口扫描，传入主机IP，实例化一个扫描对象nm
获取所有扫描协议的列表，输出所有协议扫描的开放端口以及相应端口对应的服务
'''
def PortScan(host):
    content = ""

    nm = nmap.PortScanner()
    try:
        nm.scan(host, arguments='-Pn,-sS')
        for proto in nm[host].all_protocols():
            lport = list(nm[host][proto].keys())
            for port in lport:
                if nm[host][proto][port]['state'] == "open":
                    service = nm[host][proto][port]['name']
                    content += '[*]主机' + host + ' 协议：' + proto + '\t开放端口号：' + str(port) + '\t端口服务：' + service + "\n"
        return content
    except Exception as e:
        nmap.sys.exit(0)
        raise ("nmap扫描出错，目标响应超时或存在防火墙")