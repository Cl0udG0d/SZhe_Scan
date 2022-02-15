#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2021/12/31 19:22
# @Author  : Cl0udG0d
# @File    : poclist.py
# @Github: https://github.com/Cl0udG0d
from app.utils.decorators import login_required
from app.scan import scan
from flask import (
    render_template,redirect
)

@scan.route('/poclist', methods=['GET', 'POST'])
@login_required
def poclist():
    bugbit, bugtype = core.GetBit()
    poclist = POC.query.order_by(POC.id.desc()).all()
    if request.method == 'GET':
        return render_template('pocmanage.html', bugbit=bugbit, bugtype=bugtype, poclist=poclist)
    else:
        pocname = request.form.get('pocname')
        rule = request.form.get('rule')
        expression = request.form.get('expression')
        buggrade = request.form.get('buggrade')
        redispool.hset('bugtype', pocname, buggrade)
        poc = POC(name=pocname, rule=rule, expression=expression)
        redispool.pfadd("poc", pocname)
        db.session.add(poc)
        db.session.commit()
        poclist = POC.query.order_by(POC.id.desc()).all()
        return render_template('pocmanage.html', bugbit=bugbit, bugtype=bugtype, poclist=poclist)

def test():
    print('hi')


if __name__ == '__main__':
    test()
