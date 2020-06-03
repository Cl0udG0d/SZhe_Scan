from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
'''
存放模型
'''


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    pw_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid=db.Column(db.Integer, nullable=False)
    blog=db.Column(db.String(100), nullable=True)
    signature=db.Column(db.Text, nullable=True)


# boolcheck  ->true 即 ip       ->false 即 domain
class BaseInfo(db.Model):
    __tablename__ = 'baseinfo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    boolcheck = db.Column(db.Boolean, nullable=True)
    url = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(3), nullable=False)
    title = db.Column(db.String(50), nullable=True)
    date = db.Column(db.String(30), nullable=False)
    responseheader = db.Column(db.Text, nullable=False)
    Server = db.Column(db.Text, nullable=True)
    portserver = db.Column(db.Text, nullable=True)
    sendir = db.Column(db.Text, nullable=True)


class IPInfo(db.Model):
    __tablename__ = 'ipinfo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    baseinfoid = db.Column(db.Integer, nullable=False)
    bindingdomain = db.Column(db.Text, nullable=True)
    sitestation = db.Column(db.Text, nullable=True)
    CMessage = db.Column(db.Text, nullable=False)
    ipaddr = db.Column(db.String(100), nullable=False)


class DomainInfo(db.Model):
    __tablename__ = 'domaininfo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    baseinfoid = db.Column(db.Integer, nullable=False)
    subdomain = db.Column(db.Text, nullable=True)
    whois = db.Column(db.Text, nullable=True)
    bindingip = db.Column(db.Text, nullable=True)
    sitestation = db.Column(db.Text, nullable=True)
    recordinfo = db.Column(db.Text(16777216), nullable=True)
    domainaddr = db.Column(db.String(200), nullable=True)


class BugList(db.Model):
    __tablename__ = 'buglist'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    oldurl = db.Column(db.String(50), nullable=True)
    bugurl = db.Column(db.String(200), nullable=True)
    bugname = db.Column(db.String(100), nullable=False)
    buggrade=db.Column(db.String(7),nullable=False)
    payload = db.Column(db.String(200), nullable=True)
    bugdetail = db.Column(db.Text(16777216), nullable=True)


'''
buglist表
    oldurl 扫描的原域名或IP
    bugurl 原域名或IP下的存在漏洞的一个url
    bugname 对应漏洞的名称
    buggrade 对应漏洞的等级
        serious high medium low
    payload 漏洞利用的url payload
    bugdetail 使用payload之后网页的请求源代码
    
    
'''


class POC(db.Model):
    __tablename__='poc'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.String(100),nullable=False)
    rule=db.Column(db.Text,nullable=True)
    expression=db.Column(db.Text,nullable=True)

class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)


class InvitationCode(db.Model):
    __tablename__ = 'invitationcode'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(36), nullable=False)
