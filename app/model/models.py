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
    status= db.Column(db.String(30), default='PENDING')
    starttime = db.Column(db.String(30), nullable=False)
    endtime = db.Column(db.String(30), nullable=False)

class scanTask(db.Model):
    __tablename__ = 'scanTask'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pid= db.Column(db.String(128), nullable=False)
    tid= db.Column(db.String(128), nullable=False)
    url= db.Column(db.String(128), nullable=False)
    status= db.Column(db.String(30), nullable=False, default='PENDING')
    starttime = db.Column(db.String(30), nullable=False)
    endtime = db.Column(db.String(30), nullable=False)


# boolcheck  ->true 即 ip       ->false 即 domain
class BaseInfo(db.Model):
    __tablename__ = 'baseinfo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # boolcheck = db.Column(db.Boolean, nullable=True)
    tid = db.Column(db.String(128), nullable=False)
    url = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(3))
    title = db.Column(db.String(50))
    date = db.Column(db.String(30))
    responseheader = db.Column(db.Text)
    Server = db.Column(db.Text)


class VulList(db.Model):
    __tablename__ = 'VulList'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tid = db.Column(db.String(128), nullable=False)
    url=db.Column(db.String(128))
    pocname=db.Column(db.String(128))
    result=db.Column(db.Text)
    created = db.Column(db.String(128), nullable=False)


class PocList(db.Model):
    '''
    扫描位置position 默认为前置
    '''
    __tablename__ = 'PocList'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status=db.Column(db.Boolean, default=False)
    position=db.Column(db.Boolean, default=False)
    filename=db.Column(db.String(128), nullable=False)



class pluginList(db.Model):
    __tablename__ = 'pluginList'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.Boolean, default=False)
    position = db.Column(db.Boolean, default=False)
    filename = db.Column(db.String(128), nullable=False)




class ExtList(db.Model):
    __tablename__ = 'ExtList'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tid = db.Column(db.String(128), nullable=False)
    pluginname=db.Column(db.String(128))
    result = db.Column(db.Text)
    created = db.Column(db.String(128), nullable=False)

