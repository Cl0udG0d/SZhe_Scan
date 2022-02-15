#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2021/12/31 19:18
# @Author  : Cl0udG0d
# @File    : user.py
# @Github: https://github.com/Cl0udG0d
from app.home import home
from flask import (
    render_template,redirect,request,url_for,flash,session
)
from app.model.models import *
from app.utils.decorators import login_required
from app.config.redis import redispool

@home.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    if 'name' in session or 'urls' in session:
        redispool.hset('assets', session['name'], session['urls'])
        session.pop('name')
        session.pop('urls')
    allcode = InvitationCode.query.order_by(InvitationCode.id.desc()).limit(10).all()
    user_id = session.get('user_id')
    nowuser = User.query.filter(User.id == user_id).first()
    username = nowuser.username
    photoname = redispool.hget('imagename', nowuser.email)
    if not photoname:
        photoname = 'springbird.jpg'
    profile = Profile.query.filter(Profile.userid == user_id).first()
    assetname = redispool.hkeys('assets')
    followlist = redispool.hgetall('FollowList')
    if request.method == 'GET':
        return render_template('user-center.html', allcode=allcode, username=username, profile=profile,
                               assetname=assetname, followlist=followlist, photoname=photoname)
    else:
        session['name'] = request.form.get('asset')
        session['urls'] = request.form.get('assets')
        return redirect(url_for('user'))

def test():
    print('hi')


if __name__ == '__main__':
    test()
