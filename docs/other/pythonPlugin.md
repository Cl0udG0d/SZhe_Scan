# python插件式框架开发

## 前言
在扫描一个网站的时候，在扫描的生命周期的不同阶段有一些信息是我们想要获取的：比如在一个网站的基础信息搜集之后，我们还想对它进行端口扫描；比如我们想要检测这个网站是否存在WAF，WAF的版本，如果存在WAF的话后续的扫描就不用继续执行了；又比如在获取了一个网站中的动态URL之后，我们想要得到JS文件里面的所有接口信息等等。

同时这些需求也不是所有人都需要，因为功能越多扫描起来的速度就越慢。

它们并不是一个漏洞检测POC，因为我们想要获取的是一段探测的信息，并不只有`True`，`False`两种状态

所以我们很容易想到使用插件来实现这个功能

## Python __import__() 函数
我们主要使用`__import__() `函数来实现这个功能，`__import__() `函数用于动态加载类和函数，如果一个模块经常变化就可以使用 `__import__()` 来动态载入。

用法如下

`a.py`文件
```python 
#!/usr/bin/env python    
#encoding: utf-8  
 
import os  
 
print ('在 a.py 文件中 %s' % id(os))
``` 

`test.py`文件
```python
#!/usr/bin/env python    
#encoding: utf-8  
 
import sys  
__import__('a')        # 导入 a.py 模块
``` 
执行`test.py`文件，输出结果为
> 在 a.py 文件中 4394716136

简单来说，我们只需要将插件放置在某一个特定的目录下，然后读取该目录下的全部插件，用`__import__()`函数依次执行每个插件的运行函数即可，最后统一将结果返回存储。

## 整体实现
先简单实现了这个动态调用的功能，后期根据需要继续改进插件部分的编写

```python
def scanPlugin(url,plugin,tid):
    tempPlugin = __import__("plugins.{}".format(plugin), fromlist=[plugin])
    result=tempPlugin.run(url)
    saveExts(result, tid, plugin)
``` 

`saveExts()`用来存储扫描得到的信息，`run()`函数是每个插件文件里面都需要写的，用来执行插件主体逻辑

一个端口扫描的插件如下：
```python
import re
import socket
import nmap

def run(host):
    '''
    this is portscan exts example :D
    :param host:
    :return:
    '''
    pattern = re.compile('^\d+\.\d+\.\d+\.\d+(:(\d+))?$')
    content = ""
    if not pattern.findall(host):
        host = socket.gethostbyname(host)
    if pattern.findall(host) and ":" in host:
        host=host.split(":")[0]
    nm = nmap.PortScanner()
    try:
        nm.scan(host, arguments='-Pn,-sS --host-timeout=50 --max-retries=3')
        for proto in nm[host].all_protocols():
            lport = list(nm[host][proto].keys())
            for port in lport:
                if nm[host][proto][port]['state'] == "open":
                    service = nm[host][proto][port]['name']
                    content += '[*] 主机 ' + host + ' 协议：' + proto + '\t开放端口号：' + str(port) + '\t端口服务：' + service + "\n"
        return content
    except Exception as e:
        nmap.sys.exit(0)
        pass

def test():
    print('hi')


if __name__ == '__main__':
    print(run("127.0.0.1"))
``` 
扫描本地`127.0.0.1`之后得到的结果为：
![](https://springbird3.oss-cn-chengdu.aliyuncs.com/lianxiang/20220326225820.png)

可以看到扫描端口的结果是正确的，但随之而来又存在一个新的问题，请看导入包这一部分
```python
import re
import socket
import nmap
``` 
这里的`nmap`包在我们本地的测试环境中是存在的，但是如果有用户上传的插件里面导入了一些我们没有的包，运行插件的时候自然会报错，导致插件导入之后也不能正常运行

考虑到很多编程语言都会有`预处理`这个过程，我们可以也可以对扫描器插件加载进行一次预处理，在刷新插件的时候，把插件内部需要导入，但是python环境里面不存在的包下载下来

这里只考虑了`python`脚本中按照`import requests`这种形式的导入，没有考虑变形的`from xxx import xxx`或者`from xxx import xxx as xxx`

其正则匹配规则为`pattern = re.compile("^import (.*?)$")`

一个简单的示例插件`plugin1.py`
```python
import requests
import re

def run(url):

    return "test {}".format(url)


def test():
    print('hi')


if __name__ == '__main__':
    test()
``` 
里面导入了`requests`和`re`包，实际上`requests`在我本地已经下载了,`re`是`python`内置的包

在`python`代码里面下载包的代码如下，这里直接用了清华源
```python
from pip._internal import main
def install(package,source="https://pypi.tuna.tsinghua.edu.cn/simple"):
    main(['install', package,'-i',source])
``` 

预处理的函数为
```python
def getDepends(dir):
    pattern = re.compile("^import (.*?)$")
    moduleKeys=list(sys.modules.keys())
    currdir = os.path.join(os.path.dirname(os.path.dirname(__file__)),dir)
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
``` 

`name`是我们获得的包名，`checkLib(name,moduleKeys)`函数用来检测包是否下载，未下载则返回`True`

考虑到内置包和`pip`下载包，所以在`try`里面分了两步进行
```python
def checkLib(libName,moduleKeys):
    try:
        if libName in moduleKeys:
            return False
        importlib.import_module(libName)
        return False
    except Exception as e:
        logging.warning(e)
        return True
``` 
检测结果为
![](https://springbird3.oss-cn-chengdu.aliyuncs.com/lianxiang/20220327210610.png)

使用`pip uninstall`卸载掉`requests`包，重新运行
![](https://springbird3.oss-cn-chengdu.aliyuncs.com/lianxiang/20220327210750.png)
下载成功，实现了预处理下载的功能



## 参考链接
+ `https://www.jianshu.com/p/a472f44c7161`
+ `https://www.runoob.com/python/python-func-__import__.html`
+ `https://www.jb51.net/article/232964.htm`
