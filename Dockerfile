FROM python:3.6
WORKDIR /code
ENV FLASK_APP index.py
ENV FLASK_RUN_HOST 0.0.0.0
COPY . .
RUN apt-get update && \
    apt-get install nmap -y && \
    pip install -r requirements.txt
CMD ["flask", "run"]
