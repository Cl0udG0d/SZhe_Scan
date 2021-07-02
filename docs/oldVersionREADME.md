# SZhe_Scan 碎遮Web漏洞扫描器
![](https://img.shields.io/badge/python-3.6-blue) ![](https://img.shields.io/badge/flask-1.1.1-green) ![](https://img.shields.io/badge/docker-yes-blue) ![](https://img.shields.io/badge/MySQL-%3E%3D5.5.53-brightgreen) ![](https://img.shields.io/badge/redis-%3E%3D1.0-red)

![碎遮图标.jpg](https://i.loli.net/2020/06/19/u7wmLygdJaTS2lY.jpg)

## 内容列表

- [项目时间线](#项目时间线)
- [项目特点](#项目特点)
- [项目架构](#项目架构)
- [安装方法](#安装方法)
- [运行截图](#运行截图)
- [主要功能](#主要功能)
- [如何启动](#启动)
- [扫描](#开始扫描)
- [可能会出现的问题以及解决方案](#可能会出现的问题以及解决方案)
- [修Bug交流群](#交流群)
- [碎遮名字的来由](#碎遮名字的来由)
- [后面的规划](#扫描器后面的规划)
- [作者们](#作者们简介)
- [说明](#说明)
- [致谢](#致谢)
- [赞赏码](#赞赏码)
- [留在最后](#留在最后)

### 项目时间线：

+ 2020年3月30日开始写项目第一行代码
+ 2020年6月4日项目docker打包完毕
+ .....（断断续续修复项目bug
+ 2020年10月29日，每周稳定更新...

### 项目特点：

+ 对输入的域名或IP进行自动化信息搜集与漏洞扫描，支持添加POC进行漏洞检测，扫描结果可视化显示在web界面上  
+ 使用python3编写，多线程+多进程进行资产扫描，前端使用html+css+javascript进行漏洞扫描系统的可视化，后端基于python-flask框架  
+ 使用MySQL数据库进行持久化存储，Redis数据库作为消息队列和攻击载荷payload等会大量重复使用到的数据的存储  
+ 使用邀请码注册，团队协作共用,打造良好安全生态
+ 为方便安装，将项目Docker化实现快速部署。  
### 项目架构：

![碎遮架构图.jpg](https://i.loli.net/2020/06/19/521tqXxYywUCZVB.png)

### 安装方法（择其一即可  PS：暂时不支持源码安装）：

   + WAIT ...

#### **docker安装：**

   + 在服务器或本机上安装docker以及docker-compose,网上有很多安装文章,这里不再赘述
   + (建议使用阿里云等docker加速,建议  
   + 依次输入以下三条命令:  
   > git clone https://github.com/Cl0udG0d/SZhe_Scan   
   > cd SZhe_Scan  
   > docker-compose up -d  

   + 运行结束后访问 http://ip:5000 ,默认账户登录邮箱为:springbird@qq.com,默认密码为:springbird,登录之后请第一时间修改密码:)

### 运行截图：

![登录界面.png](https://i.loli.net/2020/06/19/jfNCvX4BsPiO8mT.png)
![注册界面.png](https://i.loli.net/2020/06/19/U6ivq79DfFklJ2r.png)
![主页.png](https://i.loli.net/2020/06/11/lYEJ19wDTZ8PgiV.png)
![控制台.png](https://i.loli.net/2020/06/11/RCDdPvjFb4EgOx2.png)
![漏洞列表.png](https://i.loli.net/2020/06/12/HsQTRjbghrLnizp.png)
![漏洞详情.png](https://i.loli.net/2020/06/19/mXqYPB6AKy2QeHz.png)
![日志界面.png](https://i.loli.net/2020/06/12/4JgW32dmvTscrxu.png)
![邀请码界面.png](https://i.loli.net/2020/06/12/qLG5uFDtTJBWX2z.png)
![POC界面.png](https://i.loli.net/2020/06/12/12utocw3FilBCUO.png)
![团队.png](https://i.loli.net/2020/06/12/q3p2ToInPalfUZ4.png)
### 主要功能：

#### **信息搜集：**

##### 基础信息搜集：

   + Web指纹识别  
   + 目标状态码  
   + 标题  
   + 响应头  
   + 收录时间  
   + 端口扫描  
   + WebLogic漏洞检测 ,整合WeblogicScan项目中的WebLogic模块:https://github.com/rabbitmask/WeblogicScan
   + CMS漏洞检测,整合AngelSword项目中的几百个POC:https://github.com/Lucifer1993/AngelSword
   + 敏感目录/文件扫描
##### 深度信息搜集：

###### **域名domain**

   + 子域名收集（主动+被动）  
   + Whois信息  
   + 域名历史解析记录  
   + 域名备案信息  
   + 旁站查询  
   + 域名对应地址
###### **ip**

   + IP历史解析记录  
   + IP旁站查询  
   + C段信息扫描  
   + IP地址
#### **页面URL深度爬取：**

   + 多线程+广度优先搜索+深度爬取（默认两层）
#### **漏洞扫描 BugScan  ：**

   + SQL注入漏洞检测
   + XSS漏洞检测  
   + 命令执行漏洞检测  
   + 文件包含漏洞检测  
   + 自添加POC漏洞检测
### 启动：

   + 源码安装启动方式 在开启MySQL和Redis的情况下，命令行运行 python3 index.py，浏览器访问 127.0.0.1:5000即可  
   + docker安装启动方式 在SZhe_Scan文件夹下,使用 docker-compose up -d  启动docker服务,访问 http://ip:5000 登录进行访问
### 开始扫描：

   + 在控制台界面创建任务即可，每行输入一个url，输入的url格式可为下面四种的任意一种:
> http://www.baidu.com  
> www.baidu.com  
>http://127.0.0.1    
>127.0.0.1  
   + 支持单个url或者批量url的扫描
   + 当前的扫描速度比较慢，本月内会改进哒！！！
### 可能会出现的问题以及解决方案:

+ 问题： 如何修改头像
+ 解决方案： 项目已添加修改头像的功能，点击个人主页的头像即可进行修改
+ 问题：上传头像后个人主页头像未变化 
+ 解决方案：头像上传功能经我们检测后无错，应该是本地浏览器缓存的问题，可以上网查一下自动清空浏览器缓存的办法，或者是直接使用ctrl+f5强制刷新，即可看到修改的头像啦
### 交流群:

   > 672408351 (入群答案是U1poZVNjYW4=的base64解密，相信大师傅们是知道的
### 碎遮名字的来由:

   > 取自《有匪》一书女主用过的第二把刀的名字 ~~中二 (确实想不出啥好名字了~~    
   > 天幕如遮，唯我一刀可碎千里华盖，纵横四海而无阻  
   > 是谓碎遮
### 扫描器后面的规划:

   + 欢迎大师傅们提issue,我们看到后都会尽快回馈并修复  
   + 把已知不足的地方完善,修bug,完善自带POC和指纹信息  
   + 增加fuzz漏洞发现模块等  
   + 考虑分布式部署  
   + 如果作者们想不开的话或许会使用Go语言重写整个项目  

### 作者们简介  :

   + 重庆某大学三个大二学生  （现在已经大三啦
   > 春告鳥: 人中蔡徐坤,低配韩商言,没有情怀的白帽子  
   > 七叔: 我特别好，特别值得,特别想在忙碌与疲惫中,找到一个更好的自己  
   > 不董: 普通小孩,惟适之安
### 说明：
   > 
   > 如果项目有Bug或者意见/建议欢迎大师傅们提issue或者加入修bug专用群:672408351,如果有想要一起协作完善，长期维护这个项目的也可以联系俺  
   > 本项目仅进行信息搜集，漏洞探测工作，无漏洞利用、攻击性行为，开发初衷为仅为方便安全人员对授权项目完成测试工作和学习交流使用  
请使用者遵守当地相关法律，勿用于非授权测试，如作他用所承受的法律责任一概与作者无关，下载使用即代表使用者同意上述观点

  ### 致谢：

   + 参考借鉴并整合(~~白嫖~~)了github上很多优秀的开源扫描模块，包括但不限于:  
       https://github.com/AttackandDefenceSecurityLab/AD_WebScanner  
       https://github.com/b4ubles/python3-Wappalyzer  
       https://github.com/rabbitmask/WeblogicScan  
       https://github.com/Lucifer1993/AngelSword  
       在此对这些前辈师傅们表示由衷的感谢
   + 编写前后端的过程中遇到了不少困难，感谢队里两个天使小姐姐共同完成了扫描器的编写和可视化  

### 赞赏码：

**如果对你有帮助的话要不请作者喝杯奶茶?~~(嘿嘿)~~**  

> 开个玩笑hhh，对你有帮助已经让作者们很开心啦！:D  
> 给个Star趴  
呜呜呜，还是留个赞赏码吧，说不定大师傅愿意赞助一下卑微秃头大学生们一顿午饭呢，手动笔芯
![赞赏码2.png](https://i.loli.net/2020/06/12/aLHpmsOVMhPT31j.png)

### 留在最后

### cheer!!! 向每个为我国安全事业默默做贡献的白帽子致敬!!! :D