from exts import db
from datetime import datetime

'''
    存放所有的模型
        1，admin登录用户模型
        2，bug漏洞模型
'''
class User(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    email=db.Column(db.String(20),nullable=False)
    username=db.Column(db.String(50),nullable=False)
    password=db.Column(db.String(100),nullable=False)

class BaseInfo(db.Model):
    __tablename__='baseinfo'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    url=db.Column(db.String(50),nullable=False)
    status=db.Column(db.String(3),nullable=False)
    title=db.Column(db.String(50),nullable=True)
    date=db.Column(db.String(30),nullable=False)
    responseheader=db.Column(db.Text,nullable=False)
    Server = db.Column(db.String(100),nullable=True)
    portserver = db.Column(db.Text,nullable=True)
    senmessage = db.Column(db.Text,nullable=True)
    sendir = db.Column(db.Text,nullable=True)


class Log(db.Model):
    __tablename__='log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(50),nullable=False)
    date=db.Column(db.DateTime,default=datetime.now)