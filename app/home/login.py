#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2021/12/29 22:26
# @Author  : Cl0udG0d
# @File    : login.py
# @Github: https://github.com/Cl0udG0d

from app.home import home
from flask import (
    render_template,redirect,request,url_for,flash,session
)
from app.model.models import (
    Log,db,User
)

def save_log(ip, email,boolcheck):
    log = Log(ip=ip, email=email,boolcheck=boolcheck)
    db.session.add(log)
    db.session.commit()

@home.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('email')
        # remeber = request.form.get('remeber')
        password = request.form.get('password')
        # print("{}  {}".format(email,password))

        user = User.query.filter(User.email == email).first()
        save_log(request.remote_addr, email,user.check_password(password) if user else False)
        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('home.index'))
        else:
            flash("邮箱或密码输入错误")
            return render_template('login.html')
        

def test():
    print('hi')


if __name__ == '__main__':
    test()
