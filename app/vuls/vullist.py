#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/2/20 18:09
# @Author  : Cl0udG0d
# @File    : vullist.py
# @Github: https://github.com/Cl0udG0d
from app.vuls import vuls
from app.model.models import (
    VulList
)
from flask import (
    render_template
)
from app.utils.decorators import login_required




@vuls.route('/vuls/')
@vuls.route('/vuls/<int:page>', methods=['GET'])
@login_required
def vullist(page=1,msg=None):
    paginate = VulList.query.order_by(VulList.id.desc()).paginate(page=page, per_page=10, error_out=False)
    vuls = paginate.items
    return render_template('vullist.html', pagination=paginate, vuls=vuls)



def test():
    print('hi')


if __name__ == '__main__':
    test()
