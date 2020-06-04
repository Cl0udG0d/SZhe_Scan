# SZhe_Scan 碎遮Web漏洞扫描器  
## (该项目目前还在完善当中，预计在5月20日到5月25日之间完成碎遮1.0版本，欢迎各位大师傅们疯狂Star!!!  
![image](https://github.com/Cl0udG0d/SZhe_Scan/blob/master/static/images/%E7%A2%8E%E9%81%AE%E5%9B%BE%E6%A0%87.jpg)

## 特点  
对输入的域名或IP进行自动化信息搜集与漏洞扫描，支持添加POC进行漏洞检测，扫描结果可视化显示在web界面上  
使用python3编写，多线程+多进程进行资产扫描，前端使用html+css+javascript进行漏洞扫描系统的可视化，后端基于python-flask框架  
持久化存储使用MySQL数据库，Redis数据库作为消息队列和攻击载荷payload等会大量重复使用到的数据的存储，为了方便使用者安装，将该项目Docker化实现快速部署。  
## 项目架构  
![](https://github.com/Cl0udG0d/SZhe_Scan/blob/master/static/images/%E7%A2%8E%E9%81%AE%E6%9E%B6%E6%9E%84%E5%9B%BE.jpg)

## 安装方法(择其一即可):
   ### 源码安装(不建议使用源码安装，相比较于docker安装)
   + Python版本:3.X，数据库:MySQL，Redis 
   + Git bash界面输入 git clone git@github.com:Cl0udG0d/SZhe_Scan.git进行下载（或直接下载源代码）
   + 安装python类库: pip3 install -r requirements.txt
   + 修改config.py数据库账号密码为本地账号密码，创建MySQL数据库SZhe_Scan  
   + 命令行运行  
   > python3 manage.py db init  
   > python3 manage.py db migrate  
   > python3 manage.py db upgrade  
   三条命令映射数据库模型到数据库中  
   + 运行python3 index.py，浏览器输入127.0.0.1:5000访问漏洞扫描系统
   ### docker安装
   > 使用docker命令进行安装（暂时还未打包好，预计在5月20号之前会推出docker版本）  

## 运行截图  
![](https://github.com/Cl0udG0d/SZhe_Scan/blob/master/static/images/%E7%99%BB%E5%BD%95%E7%95%8C%E9%9D%A2.png)
![](https://github.com/Cl0udG0d/SZhe_Scan/blob/master/static/images/%E6%B3%A8%E5%86%8C%E7%95%8C%E9%9D%A2.png)
![](https://github.com/Cl0udG0d/SZhe_Scan/blob/master/static/images/%E4%B8%BB%E9%A1%B5.png)
![](https://github.com/Cl0udG0d/SZhe_Scan/blob/master/static/images/%E6%8E%A7%E5%88%B6%E5%8F%B0.png)
![](https://github.com/Cl0udG0d/SZhe_Scan/blob/master/static/images/%E6%BC%8F%E6%B4%9E%E5%88%97%E8%A1%A8.png)
![](https://github.com/Cl0udG0d/SZhe_Scan/blob/master/static/images/%E6%BC%8F%E6%B4%9E%E8%AF%A6%E6%83%85.png)
![](https://github.com/Cl0udG0d/SZhe_Scan/blob/master/static/images/%E6%97%A5%E5%BF%97%E6%96%87%E4%BB%B6.png)
![](https://github.com/Cl0udG0d/SZhe_Scan/blob/master/static/images/%E4%B8%AA%E4%BA%BA%E4%B8%AD%E5%BF%83.png)
![](https://github.com/Cl0udG0d/SZhe_Scan/blob/master/static/images/POC%E7%AE%A1%E7%90%86.png)
![](https://github.com/Cl0udG0d/SZhe_Scan/blob/master/static/images/%E5%85%B3%E4%BA%8E.png)
## 主要功能:
   ### 信息搜集:
   #### 基础信息搜集  
   + Web指纹识别  
   + 目标状态码  
   + 标题  
   + 响应头  
   + 收录时间  
   + 端口扫描  
   + WebLogic漏洞检测  
   + CMS漏洞检测（暂时还未添加，准备添加github上公开的几百个POC到碎遮的自带POC中）
   + 敏感目录/文件扫描
   #### 深度信息搜集
   ##### 域名domain  
   + 子域名收集（主动+被动）  
   + Whois信息  
   + 域名历史解析记录  
   + 域名备案信息  
   + 旁站查询  
   + 域名对应地址
   ##### IP  
   + IP历史解析记录  
   + IP旁站查询  
   + C段信息扫描  
   + IP地址
   ### 页面Url深度爬取
   + 多线程+广度优先搜索+深度爬取（默认两层）
   ### 漏洞扫描 BugScan  
   + SQL注入漏洞检测
   + XSS漏洞检测  
   + 命令执行漏洞检测  
   + 文件包含漏洞检测  
   + 自添加POC漏洞检测
## 启动
   > 源码安装启动方式 在开启MySQL和Redis的情况下，命令行运行 python3 index.py，浏览器访问 127.0.0.1:5000即可  
   > ~~docker安装启动~~ (正在快速打包啦:)
## 修Bug交流群  
   > xxxxxxxxxx 暂无
## 扫描器名字-->碎遮 的来由:
   > 取自《有匪》一书女主用过的第二把刀的名字 ~~中二 (确实想不出啥好名字了~~    
   > 天幕如遮，唯我一刀可碎千里华盖，纵横四海而无阻  
   > 是谓碎遮
## 扫描器后面的规划
   > 因为现在扫描器还比较粗糙，所以需要先把不足的地方完善，同时把发现的bug修了，完善自带POC和指纹信息，增加fuzz漏洞发现模块等，考虑分布式部署，如果作者们想不开的话或许会使用Go语言重写整个项目  
## 说明  
   > 如果项目有Bug或者意见/建议欢迎大师傅们提issue或者联系扣扣:2585614464,如果有想要一起协作完善，长期维护这个项目的也可以联系俺  
   > 本项目仅进行信息搜集，漏洞探测工作，无漏洞利用、攻击性行为，开发初衷为仅为方便安全人员对授权项目完成测试工作和学习交流使用  
   > 请使用者遵守当地相关法律，勿用于非授权测试，如作他用所承受的法律责任一概与作者无关，下载使用即代表使用者同意上述观
## 致谢  
   + 参考借鉴并整合(~~白嫖~~)了github上很多优秀的开源扫描模块，包括但不限于:  
       https://github.com/AttackandDefenceSecurityLab/AD_WebScanner  
       https://github.com/b4ubles/python3-Wappalyzer  
       https://github.com/rabbitmask/WeblogicScan  
       https://github.com/Lucifer1993/AngelSword  
       在此对这些前辈师傅们表示由衷的感谢
   + 编写前后端的过程中遇到了不少困难，感谢队里两个天使小姐姐共同完成了扫描器的编写和可视化  
   
## 如果对你有帮助的话要不请作者喝杯奶茶?~~(嘿嘿)~~  
> 开个玩笑hhh，对你有帮助已经让作者们很开心啦！:D  
> 给个Star趴
