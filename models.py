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

class Bug(db.Model):
    __tablename__='bug'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    domain=db.Column(db.String(20),nullable=False)
    ip=db.Column(db.String(20),nullable=False)
    address=db.Column(db.String(30),nullable=False)
    title=db.Column(db.String(50),nullable=False)
    status_code=db.Column(db.Integer,nullable=False)
    Server=db.Column(db.String(30),nullable=False)
    bugdetail=db.Column(db.Text,nullable=False)
    response=db.Column(db.Text,nullable=False)

class Log(db.Model):
    __tablename__='log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(50),nullable=False)
    date=db.Column(db.DateTime,default=datetime.now)
