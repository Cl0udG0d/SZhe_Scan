#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/2/19 14:56
# @Author  : Cl0udG0d
# @File    : poclist.py
# @Github: https://github.com/Cl0udG0d
import logging
import os

from app.utils.decorators import login_required
from app.pocs import poc
from flask import (
    render_template, redirect, url_for, flash, request
)
from werkzeug.utils import secure_filename
from app.model.models import (
    PocList
)
from app.model.exts import db
from init import app
from app.config import baseconfig


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in baseconfig.ALLOWED_EXTENSIONS



@poc.route('/pocs/')
@poc.route('/pocs/<int:page>', methods=['GET'])
@login_required
def poclist(page=1,msg=None):
    paginate = PocList.query.order_by(PocList.id.desc()).paginate(page=page, per_page=10, error_out=False)
    pocs = paginate.items
    return render_template('poclist.html', pagination=paginate, pocs=pocs)



@poc.route('/pocs/refresh', methods=['GET'])
@login_required
def refreshPoc():
    try:
        currdir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "../pocs/")
        poclist = PocList.query.all()
        [db.session.delete(poc) for poc in poclist]
        for files in os.listdir(currdir):
            if os.path.splitext(files)[1] == '.py':
                temptask = PocList(filename=os.path.splitext(files)[0])
                db.session.add(temptask)
        db.session.commit()
        flash('刷新成功')
    except Exception as e:
        flash('刷新失败')
        print(e)
        pass
    return redirect(url_for('pocs.poclist'))



@poc.route('/pocs/reverse/<int:id>', methods=['GET'])
@login_required
def reverse(id=None):
    try:
        poc = PocList.query.filter(PocList.id == id).first()
        poc.status=not poc.status
        db.session.commit()
    except Exception as e:
        logging.warning(e)
        pass
    return 'success'



@poc.route('/pocs/reverseAllStatus/', methods=['GET'])
@login_required
def reverseAllStatus():
    pocs = PocList.query.all()
    for poc in pocs:
        poc.status = not poc.status
    db.session.commit()
    return redirect(url_for('pocs.poclist'))



@poc.route('/pocs/uploadPoc/',methods=['POST'])
@login_required
def uploadPoc():
    for file in request.files.getlist('files'):
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(baseconfig.UPLOADED_POCS_DEST, filename))
            flash('{}上传成功'.format(filename))
        else:
            flash('上传失败')
    return redirect(url_for('pocs.poclist'))



@poc.route('/pocs/beforePoc/<int:id>',methods=['GET'])
@login_required
def beforePoc(id=None):
    try:
        poc = PocList.query.filter(PocList.id == id).first()
        poc.position=False
        db.session.commit()
    except Exception as e:
        logging.warning(e)
        return 'fail'
    return 'success'



@poc.route('/pocs/afterPoc/<int:id>',methods=['POST','GET'])
@login_required
def afterPoc(id=None):
    try:
        poc = PocList.query.filter(PocList.id == id).first()
        poc.position = True
        db.session.commit()
    except Exception as e:
        logging.warning(e)
        return 'fail'
    return 'success'

def delPocFile(filename):
    '''
    删除文件
    因为这里的文件名是安全的，所以直接进行删除
    '''
    try:
        filepath=baseconfig.UPLOADED_POCS_DEST+filename+'.py'
        os.remove(filepath)
        logging.info("del file {}".format(filepath))
    except Exception as e:
        logging.info(e)
        pass

@poc.route('/pocs/delPoc/<int:id>',methods=['GET'])
@login_required
def delPoc(id=None):
    with app.app_context():
        tempPoc= PocList.query.filter(PocList.id == id).first()
        delPocFile(tempPoc.filename)
        db.session.delete(tempPoc)
        db.session.commit()
        flash("删除成功")
    return redirect(url_for('pocs.poclist'))

@poc.route('/pocs/pocDetail/<int:id>',methods=['GET'])
def pocDetail(id=None):
    tempPoc= PocList.query.filter(PocList.id == id).first()
    if not tempPoc:
        flash('{} 加载失败'.format(id))
        return redirect(url_for('pocs.poclist'))
    filepath = baseconfig.UPLOADED_POCS_DEST + tempPoc.filename + '.py'
    file_object = open(filepath,'r', encoding='UTF-8')
    file_context = file_object.read()
    # print(file_context)
    return file_context

if __name__ == '__main__':
    print(pocDetail(1))