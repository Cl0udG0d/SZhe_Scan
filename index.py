# -*- coding:utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, session, flash
import uuid
from models import User, Log, BaseInfo, InvitationCode,BugList,POC
from exts import db
from init import app,redispool
from concurrent.futures import ThreadPoolExecutor
from SZheConsole import SZheConsole

executor = ThreadPoolExecutor()

@app.route('/<int:page>',methods=['GET'])
@app.route('/')
# @login_required
def index(page=None):
    if not page:
        page = 1
    per_page = 10
    paginate = BaseInfo.query.order_by(BaseInfo.date.desc()).paginate(page, per_page, error_out=False)
    infos = paginate.items
    return render_template('homeOne.html', paginate=paginate, infos=infos)

@app.route('/POCmanage')
def POCmanage():
    return render_template('pocmanage.html')

@app.route('/setting')
def setting():
    return render_template('setting.html')

@app.route('/editinfo')
def editinfo():
    return render_template('user-infor.html')

@app.route('/domaindetail')
def domaindetail():
    return render_template('domain-detail.html')

@app.route('/buglist/<int:page>',methods=['GET'])
@app.route('/buglist')
# @login_required
def buglist(page=None):
    if not page:
        page = 1
    per_page = 10
    paginate = BugList.query.order_by(BugList.id.desc()).paginate(page, per_page, error_out=False)
    bugs = paginate.items
    return render_template('bug-list.html', paginate=paginate, bugs=bugs)

@app.route('/bugdetail/<int:id>',methods=['GET'])
@app.route('/bugdetail')
# @login_required
def bugdetail(id=None):
    if not id:
        buginfo = BugList.query.order_by(BugList.id.desc()).first()
    else:
        buginfo = BugList.query.filter(BugList.id == id).first()
    oldurlinfo=BaseInfo.query.filter(BaseInfo.url==buginfo.oldurl).first()
    return render_template('bug-details.html',buginfo=buginfo,oldurlinfo=oldurlinfo)


@app.route('/user', methods=['GET', 'POST'])
def user():
    allcode=InvitationCode.query.order_by(InvitationCode.id.desc()).limit(10).all()
    if request.method == 'GET':
        return render_template('user-center.html',allcode=allcode)
    else:
        return render_template('user-center.html',allcode=allcode)

@app.route('/testnav')
def test_home():
    return render_template('baseOne.html')


@app.route('/test_console', methods=['GET', 'POST'])
def console():
    if request.method == 'GET':
        return render_template('console.html')
    else:
        urls = request.form.get('urls')
        executor.submit(SZheConsole, urls)
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
        password = User.check_password(request.form.get('password'))
        if user and password:
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


# 生成邀请码
@app.route('/GenInvitationCode', methods=['GET', 'POST'])
def GenInvitationCode():
    code = str(uuid.uuid1())
    Code = InvitationCode(code=code)
    db.session.add(Code)
    db.session.commit()
    allcode=InvitationCode.query.order_by(InvitationCode.id.desc()).limit(10).all()
    return render_template("user-center.html", temp=Code.code,allcode=allcode)

def AddPOC():
    pocname=""
    rule=""
    expression=""
    buggrade=""
    redispool.hset('bugtype',pocname,buggrade)
    poc = POC(name=pocname, rule=rule,expression=expression)
    db.session.add(poc)
    db.session.commit()

@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('sign_up.html')
    else:
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        invitationcode = request.form.get('invitationcode')
        # 邮箱和用户名验证
        message = validate(email, username, password1, password2)
        # 邀请码验证
        IsCode = InvitationCode.query.filter(InvitationCode.code == invitationcode).first()
        if message:
            flash(message)
            return render_template('sign_up.html')
        elif IsCode is None:
            flash("邀请码错误")
            return render_template('sign_up.html')
        else:
            user = User(email=email, username=username, password=password1)
            db.session.add(user)
            db.session.delete(IsCode)
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




# 日志每页显示30条
@app.route('/log_detail/')
@app.route('/log_detail/<int:page>', methods=['GET'])
# @login_required
def log_detail(page=None):
    if not page:
        page = 1
    # page = int(request.args.get('page', 1))
    # per_page = int(request.args.get('per_page', 2))
    per_page = 38
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
    app.run()
