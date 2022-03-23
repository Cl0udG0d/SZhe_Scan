# 碎遮-风起

> 一款开源的轻量Web漏洞扫描器

## 简介

现在的扫描器越来越重，对于目标全面的信息搜集会花费很长的时间，而有的选项并不是我们需要的，很多时候我们需要的是一个轻量快速扫描的Web扫描器

举一个简单的例子，当你需要用到端口扫描的时候，只需要编写一个前置的端口扫描插件，上传并应用这个插件，就能够在扫描的过程中得到对应目标的端口扫描信息。当存在一个新的影响范围大的漏洞时你从fofa上获取到了可能存在漏洞的IP列表，你把你编写的基于pocsuite3的检测代码上传之后就能够快速扫描。你说你的POC是yaml格式的？没关系，后期我们也会对yaml格式的POC进行兼容。

在这些情况下原有的大型扫描器可能不太适用，所以我重构了原来的碎遮扫描器

扫描器砍掉了非必要和耗时比较长的信息收集部分，用户可以自定义POC和插件来进行扫描，POC和插件支持本地上传，相关文档如下:

+ [Pocsuite3 开发文档及 PoC 编写规范及要求说明](./other/CODING.md)
+ [python实现插件框架]()
+ [插件编写]()


项目使用了以下技术：
+ flask+mysql+redis+celery+tornado
+ 轻量级扫描器
+ docker部署
+ 基于pocsuite3的poc部署
+ 自编写插件易扩展
+ ...


## 快速开始 

docker安装 
```bash
git clone git@github.com:Cl0udG0d/SZhe_Scan.git
cd SZhe_Scan
docker-compose up -d 
``` 

访问ip:8000 即可，默认账户密码为:admin@admin.com / admin 

选择需要的POC和插件，添加任务进行扫描即可


## 开发团队

<div style="display: flex;padding: 25px 0;border-bottom: 1px dotted #ddd;">
    <div class="avatar" style="flex: 0 0 80px;display: block;">
        <img src="https://avatars.githubusercontent.com/u/45556496" width="80" height="80" style="border-radius: 50%;object-fit: cover;max-width: 100%;">
    </div>
    <div class="profile" style="padding-left: 26px;flex: 1;display: block;">
        <h3 style="margin: 0;font-size: 1.3em;">
            春告鳥
        </h3>
        <dl>
            <dt style="text-transform: uppercase;font-size: 0.84em;font-weight: 600;">CTFer && 安全开发 && 漏洞挖掘</dt>
            <dt style="font-weight: 600;">
                <a href="https://www.cnblogs.com/Cl0ud/" target="_blank">https://www.cnblogs.com/Cl0ud/
                </a>
            </dt>
        </dl>
    </div>
</div>

## 常见问题 

## 联系我们
- 提交一个[issue](https://github.com/Cl0udG0d/SZhe_Scan/issues/new)
- 想要一起完善这个项目欢迎给我发邮件加入作者群：[2585614464@qq.com](mailto:2585614464@qq.com)
- 如需合作可联系微信：Cl0udG0d

欢迎添加我微信备注`进群`，一起来聊天吹水哇，以及一个会发布安全学习相关内容的公众号，欢迎关注 :)


<div>
    <img  alt="JPG" src="https://github.com/Cl0udG0d/Cl0udG0d/raw/main/images/cgn.jpg"  width="170px" />
    <img  alt="JPG" src="https://github.com/Cl0udG0d/Cl0udG0d/raw/main/images/gzh.jpg"  width="170px" />
</div>
