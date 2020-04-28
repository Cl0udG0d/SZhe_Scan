# SZhe_Scan 碎遮Web漏洞扫描器

## 特点
 对输入的域名或IP进行自动化信息搜集与漏洞扫描，支持添加POC进行漏洞检测，扫描结果可视化显示在web界面上
 使用python3编写，多线程+多进程进行资产扫描，前端 html+css+javascript ，后端基于python flask框架，数据库使用redis+MySQL

## 安装方法(择其一即可):
   ### 本地安装
   > python版本要求：3.x
   > 执行 pip3 install -r requirements.txt 进行类库的下载
   > 修改config.py中MySQL数据库的账号和密码为自己的
   
   ### docker安装
   > 使用docker命令进行安装

## 主要功能:
   ### 信息搜集:
   #### 基础信息搜集
       - Web指纹识别
       - 网页状态码
       - 网页标题
       - 目标响应头
       - 敏感目录文件发现
       - 端口开放情况
       - 地址信息
   #### 深度信息搜集
   ##### 域名domain
        - 子域名搜集（主动+被动）
        - Whois信息
        - BindingIP
        - DomainRecordInfo
        - SiteStation
   ##### IP
        - BingdingDomain
        - GetSiteStation
        - C段信息搜集 CMessage
   ### 页面Url深度爬取
        - 多线程广度优先搜索
   ### 漏洞扫描 BugScan
        - SQL注入漏洞检测
        - XSS漏洞检测
        - 命令执行漏洞检测
        - 文件包含漏洞检测
        - WebLogic漏洞检测
        - POC 漏洞检测
   
## 启动
   > 源码安装启动 python3 index.py，浏览器访问 127.0.0.1:5000即可
   > docker安装启动 

## 感谢
   编写的过程中遇到了不少的困难，感谢队里两个天使小姐姐共同完成了扫描器的编写和可视化
   
## 修Bug交流群
    > xxxxxxxxxxx


## 扫描器名字的来由:
   > 猜?

## 扫描器后面的完善
   > 把发现的bug修了，完善自带POC和指纹信息，考虑分布式部署，如果作者们想不开的话或许会使用Golang重写整个项目
   
## 如果有帮助到你的话可否请作者们喝杯奶茶呢?
