#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2021/12/31 19:18
# @Author  : Cl0udG0d
# @File    : user.py
# @Github: https://github.com/Cl0udG0d
from app.home import home
from flask import (
    render_template,redirect,request,url_for,session,flash
)
from app.model.models import (
    User,db
)
from app.utils.decorators import login_required




@login_required
@home.route('/editPasswd', methods=['POST'])
def editPasswd():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('home.login'))
    oldpasswd = request.form.get('oldpasswd')
    newpasswd = request.form.get('newpasswd')

    nowuser = User.query.filter(User.id == user_id).first()

    if nowuser.check_password(oldpasswd):
        nowuser.set_password(newpasswd)
        db.session.commit()
        return redirect(url_for('home.login'))
    else:
        flash("旧密码输入错误 :(")
        return redirect(url_for('home.index'))




def test():
    print('hi')


if __name__ == '__main__':
    test()
