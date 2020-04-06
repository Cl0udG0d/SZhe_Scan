# -*- coding:utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, session
from flask import Flask,render_template,request,redirect,url_for,session,flash
import config
from models import User, Log
from exts import db
from decorators import login_required

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


def save_log(ip, email, password):
    log = Log(ip=ip, email=email, password=password)
    db.session.add(log)
    db.session.commit()


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('sign_in.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        remeber = request.form.get('remeber')
        save_log(request.remote_addr, email, password)
        user = User.query.filter(User.email == email, User.password == password).first()
        if user:
            if remeber:
                session.permanent = True
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            flash("邮箱或密码输入错误")
            return render_template('sign_in.html')

def validate(email,username,password1,password2):
    user_email = User.query.filter(User.email == email).first()
    user_name = User.query.filter(User.username == username).first()
    if user_email:
        return "邮箱已被注册"
    elif len(username)<4:
        return "用户名长度至少四个字符"
    elif user_name:
        return "用户名已被注册"
    elif len(password1)<6:
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
        email=request.form.get('email')
        username=request.form.get('username')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        #邮箱和用户名验证
        message=validate(email,username,password1,password2)
        if message:
            flash(message)
            return render_template('sign_up.html')
        else:
            user = User(email=email, username=username, password=password1)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))


@app.route('/logout/')
@login_required
def logout():
    # session.pop('user_id')
    # del session('user_id')
    session.clear()
    return redirect(url_for('login'))


@app.route('/home/')
@login_required
def home():
    return render_template('home.html')


@app.route('/bug_list/')
@login_required
def bug_list():
    return render_template('bug_list.html')


@app.route('/log_detail/')
@login_required
def log_detail():
    context = {
        'logs': Log.query.order_by(Log.date.desc()).all()
    }
    return render_template('log_detail.html', **context)


@app.context_processor
def my_comtext_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
    return {}


if __name__ == '__main__':
    app.run()
