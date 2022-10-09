FROM python:3.6
WORKDIR /
COPY . .
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install aptitude -y && \
    mv /etc/apt/sources.list /etc/apt/sources.list.bak && \
    echo "deb http://mirrors.aliyun.com/debian stretch main contrib non-free" >/etc/apt/sources.list && \
    echo "deb-src http://mirrors.aliyun.com/debian stretch main contrib non-free" >>/etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian stretch-updates main contrib non-free" >>/etc/apt/sources.list && \
    echo "deb-src http://mirrors.aliyun.com/debian stretch-updates main contrib non-free" >>/etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian-security stretch/updates main contrib non-free" >>/etc/apt/sources.list && \
    echo "deb-src http://mirrors.aliyun.com/debian-security stretch/updates main contrib non-free" >>/etc/apt/sources.list && \
    echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" >>/etc/apt/sources.list && \
#     wget http://www.linuxidc.com/files/repo/google-chrome.list -P /etc/apt/sources.list.d/ && \
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub  | apt-key add - && \
    aptitude update && \
    aptitude install google-chrome-stable -y && \
    wget --no-check-certificate --content-disposition https://github.com/Qianlitp/crawlergo/releases/download/v0.4.3/crawlergo_linux_amd64 -O crawlergo && \
    chmod 777 crawlergo && \
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
CMD ["python", "server.py"]