# -*- coding:utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from lxml.html.builder import HEAD
import config
from models import User, Log, BaseInfo
from exts import db
from BaseMessage import GetBaseMessage
import json
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
executor = ThreadPoolExecutor()


@app.route('/')
def index():
    return render_template('homeOne.html')


def InfoCommit(url):
    Info = GetBaseMessage(url)
    try:
        with app.app_context():
            db.session.add(BaseInfo(url=url, status=Info.GetStatus(), title=Info.GetTitle(), date=Info.GetDate(),
                                    responseheader=Info.GetResponseHeader(),
                                    Server=Info.GetFinger(), portserver=Info.PortScan(), senmessage=Info.SenMessage(),
                                    sendir="test"))
            db.session.commit()
    except Exception:
        pass


@app.route('/testMySQL')
def testmysql():
    url = "blog.csdn.net"
    executor.submit(InfoCommit, url)
    # Info = BaseInfo.query.filter(BaseInfo.id == 2).first()
    return "hi!"


@app.route('/user')
def user():
    return render_template('user-center.html')


@app.route('/testnav')
def test_home():
    return render_template('baseOne.html')


@app.route('/test_console')
def console():
    return render_template('console.html')


def save_log(ip, email):
    log = Log(ip=ip, email=email)
    db.session.add(log)
    db.session.commit()


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('sign_in.html')
    else:
        email = request.form.get('email')
        remeber = request.form.get('remeber')
        save_log(request.remote_addr, email)
        user = User.query.filter(User.email == email).first()
        if user:
            if remeber:
                session.permanent = True
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            flash("邮箱或密码输入错误")
            return render_template('sign_in.html')


def validate(email, username, password1, password2):
    user_email = User.query.filter(User.email == email).first()
    user_name = User.query.filter(User.username == username).first()
    if user_email:
        return "邮箱已被注册"
    elif len(username) < 4:
        return "用户名长度至少四个字符"
    elif user_name:
        return "用户名已被注册"
    elif len(password1) < 6:
        return "密码长度至少6个字符"
    elif password1 != password2:
        return "两次密码输入不一致"
    else:
        return


@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('sign_up.html')
    else:
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        # 邮箱和用户名验证
        message = validate(email, username, password1, password2)
        if message:
            flash(message)
            return render_template('sign_up.html')
        else:
            user = User(email=email, username=username, password=password1)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))


@app.route('/logout/')
# @login_required
def logout():
    # session.pop('user_id')
    # del session('user_id')
    session.clear()
    return redirect(url_for('login'))


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/home/')
# @login_required
def home():
    return render_template('home.html')


@app.route('/bug_list/')
# @login_required
def bug_list():
    return render_template('bug_list.html')


# 日志每页显示30条
@app.route('/log_detail/')
@app.route('/log_detail/<int:page>', methods=['GET'])
# @login_required
def log_detail(page=None):
    if not page:
        page = 1
    # page = int(request.args.get('page', 1))
    # per_page = int(request.args.get('per_page', 2))
    per_page = 30
    paginate = Log.query.order_by(Log.date.desc()).paginate(page, per_page, error_out=False)
    logs = paginate.items
    return render_template('log_detail.html', paginate=paginate, logs=logs)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/test500')
def test500():
    return render_template('500.html')


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.context_processor
def my_comtext_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
    return {}


if __name__ == '__main__':
    # ImportToRedis.ToRedis()
    app.run()
