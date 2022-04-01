# Ubuntu系统 docker-compose安装 

## 下载docker-compose 
```bash 
sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
``` 

## 设置可执行权限
```bash
sudo chmod +x /usr/local/bin/docker-compose
``` 

## 检查是否安装成功
```bash
docker-compose --version
``` 

这将打印出我们安装的版本：
```bash
root@VM-4-5-ubuntu:/home/ubuntu# docker-compose --version
docker-compose version 1.21.2, build a133471
``` 