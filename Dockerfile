FROM python:3.6
WORKDIR /code
ENV FLASK_APP index.py
ENV FLASK_RUN_HOST 0.0.0.0
COPY . .
RUN apt-get update && \
    apt-get install nmap -y && \
<<<<<<< HEAD
    pip install -r requirements.txt
=======
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
>>>>>>> 13cdacd6cf9f71f63c31fdc15347590f723efd1e
CMD ["flask", "run"]
