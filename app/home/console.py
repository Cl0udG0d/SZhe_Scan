#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2021/12/31 19:21
# @Author  : Cl0udG0d
# @File    : console.py
# @Github: https://github.com/Cl0udG0d
from app.utils.decorators import login_required
from app.home import home
from flask import (
    render_template,redirect,request,url_for,session
)
from app.model.models import *

@home.route('/test_console', methods=['GET', 'POST'])
@login_required
def console():
    bugbit, bugtype = core.GetBit()
    counts = core.GetCounts()
    ports = core.GetPort()
    services = core.GetServices()
    target = core.GetTargetCount()
    if 'targetscan' in session:
        urls = session['targetscan'].split()
        redispool.hincrby('targetscan', 'waitcount', len(urls))
        for url in urls:
            queue.enqueue(SZheScan, url)
            # SZheScan.delay(url)
        session.pop('targetscan')
    try:
        lastscantime = BaseInfo.query.order_by(BaseInfo.id.desc()).first().date
    except:
        lastscantime = "暂无扫描"
        pass
    if request.method == 'GET':
        return render_template('console.html', bugbit=bugbit, bugtype=bugtype, counts=counts, lastscantime=lastscantime,
                               ports=ports, services=services, target=target)
    else:
        session['targetscan'] = request.form.get('urls')
        return redirect(url_for('console'))

def test():
    print('hi')


if __name__ == '__main__':
    test()
