# Windows下源码安装教程

个人不建议`Windows`源码安装,因为比较繁琐,源码安装只针对有`flask`开发基础并想要二改的朋友,有新的想法和功能欢迎提pull

## 背景
+ windows11

## 安装软件 
+ python3
 
    我用的3.6,版本新一点无所谓
+ mysql 
    
    这里我为了方便用的phpmyadmin,当然可以只安装mysql
+ redis 
    
    Redis 官方不建议在 windows 下使用 Redis，所以官网没有 windows 版本可以下载。还好微软团队维护了开源的 windows 版本，虽然只有 3.2 版本，对于普通测试使用足够了

    https://www.redis.com.cn/redis-installation.html

## 安装启动
下载项目源代码
```bash
git clone https://github.com/Cl0udG0d/SZhe_Scan 
``` 

进入`SZhe_Scan`文件夹
```bash 
cd SZhe_Scan
``` 

`pip`安装`python`包

`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`

启动`MySQL`,并将`SZhe_Scan/mysql/init/init.sql`文件导入,初始化数据库

修改`SZhe_Scan/app/config/baseconfig.py`中数据库账户密码为本地账户密码

启动`Redis-Server`

命令行启动`celery`服务
```bash
celery -A app.celery.celerytask:scantask worker -c 10 --loglevel=info -P eventlet
``` 

启动`flask`服务
```bash
python server.py
``` 

服务启动在本地`8000`端口,登录用户名密码为: admin@admin.com / admin
