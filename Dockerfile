FROM python:3.6
WORKDIR /code
ENV FLASK_APP index.py
ENV FLASK_RUN_HOST 0.0.0.0
COPY . .
RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
    apt-get update && \
    apt-get install nmap -y && \
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
CMD ["flask", "run"]