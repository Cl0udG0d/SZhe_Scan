# -*- coding: UTF-8 -*-
import os
import re
import sys
import time

file_ext = ('.eot', '.svg', '.tff', '.woff', '.png', '.jpg', '.css', '.js', '.html')
text_file_ext = ('.css', '.js', '.html')
exclude_files = ('index.html')

files = {}

file_refers = {}

## Linux/MacOS 下直接删除文件
# command = '/bin/rm {}/{}'


## 显示文件列表，如果需要备份可先形成，可以 python asset_cleaner.py | xargs tar cvf asset.bak.tar
# command = '{}/{}'


def findstring(pathfile, target):
    fp = open(pathfile, "r")
    strr = fp.read()

    if (strr.find("set_commission") != -1):
        return True
    return False


def listPathFile(path='.'):
    resultSet=set()
    pattern1 = re.compile("filename='(.*?)'")
    pattern2 = re.compile('<link href="../static/(.*?)" rel="stylesheet">')
    pattern3 = re.compile('<script src="../static/(.*?)"></script>')

    for parent, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath=os.path.join(path,filename)
            # print(filepath)
            f=open(filepath,"r",encoding='utf-8')
            for line in f.readlines():
                line=line.strip()
                result1=pattern1.findall(line)
                result2=pattern2.findall(line)
                result3=pattern3.findall(line)
                if (result1 and result1[0] not in resultSet):
                    resultSet.add(result1[0])
                    # print(result1[0])
                elif (result2 and result2[0] not in resultSet):
                    resultSet.add(result2[0])
                    # print(result2[0])
                elif  (result3 and result3[0] not in resultSet):
                    resultSet.add(result3[0])
                    # print(result3[0])
                # if "filename" in line:
                #     print(line)
            # f = open("c:\\1.txt", "r")
            # lines = f.readlines()  # 读取全部内容 ，并以列表方式返回
            # for line in lines:
            #     print(line)
            # print(filename)
            # if os.path.splitext(filename)[1] in file_ext and not filename in exclude_files:
            #     files.update({filename: parent})
            #     file_refers.update({filename: False})
    newlist=list(resultSet)
    newlist.sort()
    for i in newlist:
        print(i)
    return

# for parent, dirnames, filenames in os.walk('.'):
#     for filename in filenames:
#         if os.path.splitext(filename)[1] in file_ext and not filename in exclude_files:
#             files.update({filename: parent})
#             file_refers.update({filename: False})
#
# for parent, dirnames, filenames in os.walk('.'):
#     for openfile in filenames:
#         if not os.path.splitext(openfile)[1] in text_file_ext:
#             continue
#
#         try:
#             fp = open(parent + "/" + openfile, "r")
#             file_string = fp.read()
#
#             for filename in files:
#                 if file_string.find(filename) >= 0:
#                     file_refers.update({filename: True})
#
#             fp.close()
#         except Exception as err:
#             sys.stderr.write(parent + '/' + openfile + ':' + "{}\n".format(err))
#             continue
#
# sys.stderr.write("未引用的文件如下：\n---------------------------\n")
# time.sleep(0.1)
# for file in file_refers:
#     if not file_refers[file]:
#         print("{} {}".format(files[file], file))
#         # print(command.format(files[file], file))
# time.sleep(0.1)
# sys.stderr.write("------------结束-----------\n")


def main():
    path="./assets/templates"
    listPathFile(path)
    return

if __name__ == '__main__':
    main()