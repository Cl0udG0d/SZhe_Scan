import sys
import poc.Console
import poc.CVE_2014_4210
import poc.CVE_2016_0638
import poc.CVE_2016_3510
import poc.CVE_2017_3248
import poc.CVE_2017_3506
import poc.CVE_2017_10271
import poc.CVE_2018_2628
import poc.CVE_2018_2893
import poc.CVE_2018_2894
import poc.CVE_2019_2725
import poc.CVE_2019_2729

'''
白嫖魔改自rabbitmask师傅的Weblogic一键漏洞检测工具，V1.3
https://github.com/rabbitmask/WeblogicScan

修改weblogicscan位置 到最开始基础信息搜集处，检测输入的域名或ip是否存在weblogic漏洞
并且直接将结果存储在buglist表中
'''


def PocS(rip,rport):
    result=[]
    print('[*]Console path is testing...')
    try:
        result.append(poc.Console.run(rip, rport))
    except:
        print ("[-]Target Weblogic console address not found.")

    print('[*]CVE_2014_4210 is testing...')
    try:
        result.append(poc.CVE_2014_4210.run(rip, rport))
    except:
        print ("[-]CVE_2014_4210 not detected.")

    print('[*]CVE_2016_0638 is testing...')
    try:
        result.append(poc.CVE_2016_0638.run(rip, rport, 0))
    except:
        print ("[-]CVE_2016_0638 not detected.")

    print('[*]CVE_2016_3510 is testing...')
    try:
        result.append(poc.CVE_2016_3510.run(rip, rport, 0))
    except:
        print ("[-]CVE_2016_3510 not detected.")

    print('[*]CVE_2017_3248 is testing...')
    try:
        result.append(poc.CVE_2017_3248.run(rip, rport, 0))
    except:
        print ("[-]CVE_2017_3248 not detected.")

    print('[*]CVE_2017_3506 is testing...')
    try:
        result.append(poc.CVE_2017_3506.run(rip, rport, 0))
    except:
        print ("[-]CVE_2017_3506 not detected.")

    print('[*]CVE_2017_10271 is testing...')
    try:
        result.append(poc.CVE_2017_10271.run(rip, rport, 0))
    except:
        print("[-]CVE_2017_10271 not detected.")

    print('[*]CVE_2018_2628 is testing...')
    try:
        result.append(poc.CVE_2018_2628.run(rip, rport, 0))
    except:
        print("[-]CVE_2018_2628 not detected.")

    print('[*]CVE_2018_2893 is testing...')
    try:
        result.append(poc.CVE_2018_2893.run(rip, rport, 0))
    except:
        print("[-]CVE_2018_2893 not detected.")

    print('[*]CVE_2018_2894 is testing...')
    try:
        result.append(poc.CVE_2018_2894.run(rip, rport, 0))
    except:
        print("[-]CVE_2018_2894 not detected.")

    print('[*]CVE_2019_2725 is testing...')
    try:
        result.append(poc.CVE_2019_2725.run(rip, rport, 0))
    except:
        print("[-]CVE_2019_2725 not detected.")

    print('[*]CVE_2019_2729 is testing...')
    try:
        result.append(poc.CVE_2019_2729.run(rip, rport, 0))
    except:
        print("[-]CVE_2019_2729 not detected.")

    print ("[*]Happy End,the goal is {}:{}".format(rip,rport))

def run(url):
    if ":" not in url:
        return False
    ip=url.split(":")[0]
    port=url.split(":")[1]
    PocS(ip,port)
    # if len(sys.argv)<3:
    #     print('Usage: python3 WeblogicScan [IP] [PORT]')
    # else:
    #     url = sys.argv[1]
    #     port = int(sys.argv[2])
    #     PocS(url,port)

if __name__ == '__main__':
    run("127.0.0.1:80")