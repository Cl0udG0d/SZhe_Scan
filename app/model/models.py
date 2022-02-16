from app.model.exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

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



class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    boolcheck = db.Column(db.Boolean, nullable=True)
    date = db.Column(db.DateTime, default=datetime.now)



class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tid= db.Column(db.String(128), nullable=False)
    name= db.Column(db.String(128), nullable=False)
    starttime = db.Column(db.String(30), nullable=False)
    endtime = db.Column(db.String(30), nullable=False)
    key=db.Column(db.String(24), nullable=False)

class scanTask(db.Model):
    __tablename__ = 'scanTask'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tid= db.Column(db.String(128), nullable=False)
    starttime = db.Column(db.String(30), nullable=False)
    endtime = db.Column(db.String(30), nullable=False)
    key=db.Column(db.String(128), nullable=False)


# boolcheck  ->true 即 ip       ->false 即 domain
# class BaseInfo(db.Model):
#     __tablename__ = 'baseinfo'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     boolcheck = db.Column(db.Boolean, nullable=True)
#     url = db.Column(db.String(50), nullable=False)
#     status = db.Column(db.String(3), nullable=False)
#     title = db.Column(db.String(50), nullable=True)
#     date = db.Column(db.String(30), nullable=False)
#     responseheader = db.Column(db.Text, nullable=False)
#     Server = db.Column(db.Text, nullable=True)
#     portserver = db.Column(db.Text, nullable=True)
#     sendir = db.Column(db.Text, nullable=True)
#
#
# class IPInfo(db.Model):
#     __tablename__ = 'ipinfo'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     baseinfoid = db.Column(db.Integer, nullable=False)
#     bindingdomain = db.Column(db.Text, nullable=True)
#     sitestation = db.Column(db.Text, nullable=True)
#     CMessage = db.Column(db.Text, nullable=False)
#     ipaddr = db.Column(db.String(100), nullable=False)
#
#
# class DomainInfo(db.Model):
#     __tablename__ = 'domaininfo'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     baseinfoid = db.Column(db.Integer, nullable=False)
#     subdomain = db.Column(db.Text, nullable=True)
#     whois = db.Column(db.Text, nullable=True)
#     bindingip = db.Column(db.Text, nullable=True)
#     sitestation = db.Column(db.Text, nullable=True)
#     recordinfo = db.Column(db.Text(16777216), nullable=True)
#     domainaddr = db.Column(db.String(200), nullable=True)


# class BugList(db.Model):
#     __tablename__ = 'buglist'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     oldurl = db.Column(db.String(50), nullable=True)
#     bugurl = db.Column(db.String(200), nullable=True)
#     bugname = db.Column(db.String(100), nullable=False)
#     buggrade = db.Column(db.String(7), nullable=False)
#     payload = db.Column(db.String(200), nullable=True)
#     bugdetail = db.Column(db.Text(16777216), nullable=True)




