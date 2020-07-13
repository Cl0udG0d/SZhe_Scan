import os
from flask import render_template, request, redirect, url_for, session, flash
import uuid
from models import User, Log, BaseInfo, InvitationCode, BugList, POC, IPInfo, DomainInfo, Profile
from exts import db
from init import app, redispool
import core
from decorators import login_required
from config import queue
from SZheConsole import SZheScan



def save_log(ip, email):
    log = Log(ip=ip, email=email)
    db.session.add(log)
    db.session.commit()


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


'''
    输入的url格式为:
        www.baidu.com
        127.0.0.1
        http://www.baidu.com
        http://127.0.0.1
    每行一个
'''


@app.route('/<int:page>', methods=['GET'])
@app.route('/')
@login_required
def index(page=None):
    bugbit, bugtype = core.GetBit()
    if not page:
        page = 1
    per_page = 10
    paginate = BaseInfo.query.order_by(BaseInfo.date.desc()).paginate(page, per_page, error_out=False)
    infos = paginate.items
    return render_template('homeOne.html', paginate=paginate, infos=infos, bugbit=bugbit, bugtype=bugtype)


@app.route('/POCmanage', methods=['GET', 'POST'])
@login_required
def POCmanage():
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


@app.route('/editinfo', methods=['GET', 'POST'])
@login_required
def editinfo():
    user_id = session.get('user_id')
    nowuser = User.query.filter(User.id == user_id).first()
    if request.method == 'GET':
        username = nowuser.username
        profile = Profile.query.filter(Profile.userid == user_id).first()
        if not profile:
            signature = ""
            blog = ""
        else:
            signature = profile.signature
            blog = profile.blog
        # print("hi! {} {} {}".format(username, blog, signature))
        return render_template('user-infor.html', username=username, blog=blog, signature=signature)
    else:
        username = request.form.get('username')
        blog = request.form.get('blog')
        signature = request.form.get('signature')
        oldpassword = request.form.get('oldpassword')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if nowuser.check_password(oldpassword):
            if password1 != password2:
                flash("两次密码输入不一致 :D")
                return render_template('user-infor.html')
            else:
                profile = Profile.query.filter(Profile.userid == user_id).first()
                if not profile:
                    temp = Profile(userid=user_id, blog=blog, signature=signature)
                    db.session.add(temp)
                elif username != "" and blog != "" and signature != "":
                    profile.blog = blog
                    profile.signature = signature
                nowuser.username = username
                nowuser.set_password(password1)
                db.session.commit()
                return redirect(url_for('user'))
        else:
            flash("旧密码输入错误 :(")
            return render_template('user-infor.html', username=username, blog=blog, signature=signature)


@app.route('/domaindetail/<int:id>', methods=['GET'])
@app.route('/domaindetail')
@login_required
def domaindetail(id=None):
    bugbit, bugtype = core.GetBit()
    if not id:
        baseinfo = BaseInfo.query.order_by(BaseInfo.id.desc()).first()
        if not baseinfo:
            return "请添加扫描任务"
    else:
        baseinfo = BaseInfo.query.filter(BaseInfo.id == id).order_by(BaseInfo.id.desc()).first()
    if baseinfo.boolcheck:
        deepinfo = IPInfo.query.filter(IPInfo.baseinfoid == baseinfo.id).first()
    else:
        deepinfo = DomainInfo.query.filter(DomainInfo.baseinfoid == baseinfo.id).order_by(DomainInfo.id.desc()).first()
    buglist = BugList.query.filter(BugList.oldurl == baseinfo.url).all()
    return render_template('domain-detail.html', baseinfo=baseinfo, deepinfo=deepinfo, buglist=buglist, bugbit=bugbit,
                           bugtype=bugtype)


@app.route('/buglist/<int:page>', methods=['GET'])
@app.route('/buglist')
@login_required
def buglist(page=None):
    bugbit, bugtype = core.GetBit()
    if not page:
        page = 1
    per_page = 10
    paginate = BugList.query.order_by(BugList.id.desc()).paginate(page, per_page, error_out=False)
    bugs = paginate.items
    return render_template('bug-list.html', paginate=paginate, bugs=bugs, bugbit=bugbit, bugtype=bugtype)


@app.route('/bugdetail/<int:id>', methods=['GET', 'POST'])
@app.route('/bugdetail')
@login_required
def bugdetail(id=None):
    bugbit, bugtype = core.GetBit()
    if not id:
        buginfo = BugList.query.order_by(BugList.id.desc()).first()
    else:
        buginfo = BugList.query.filter(BugList.id == id).first()
    oldurlinfo = BaseInfo.query.filter(BaseInfo.url == buginfo.oldurl).first()
    if redispool.hexists('FollowList', buginfo.id):
        flag = False
    else:
        flag = True
    if request.method == 'GET':
        return render_template('bug-details.html', buginfo=buginfo, oldurlinfo=oldurlinfo, bugbit=bugbit,
                               bugtype=bugtype, flag=flag)
    else:
        redispool.hset('FollowList', buginfo.id, buginfo.bugurl)
        return render_template('bug-details.html', buginfo=buginfo, oldurlinfo=oldurlinfo, bugbit=bugbit,
                               bugtype=bugtype, flag=False)


@app.route('/assetdetail/')
@app.route('/assetdetail/<name>', methods=['GET'])
@login_required
def assetdetail(name=None):
    if not name:
        return redirect(url_for('index'))
    else:
        assetdetail = redispool.hget('assets', name)
        return render_template('assetDetail.html', name=name, assetdetail=assetdetail)


@app.route('/user', methods=['GET', 'POST'])
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
        session['name']=request.form.get('asset')
        session['urls']=request.form.get('assets')
        return redirect(url_for('user'))


@app.route('/test_console', methods=['GET', 'POST'])
@login_required
def console():
    bugbit, bugtype = core.GetBit()
    counts = core.GetCounts()
    ports = core.GetPort()
    services = core.GetServices()
    target = core.GetTargetCount()
    if 'targetscan' in session:
        urls=session['targetscan'].split()
        redispool.hincrby('targetscan', 'waitcount', len(urls))
        for url in urls:
            queue.enqueue(SZheScan,url)
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
        session['targetscan']=request.form.get('urls')
        return redirect(url_for('console'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('sign_in.html')
    else:
        email = request.form.get('email')
        remeber = request.form.get('remeber')
        password = request.form.get('password')
        # print("{} {} {}".format(email,remeber,password))
        save_log(request.remote_addr, email)
        user = User.query.filter(User.email == email).first()
        if user and user.check_password(password):
            if remeber:
                session.permanent = True
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            flash("邮箱或密码输入错误")
            return render_template('sign_in.html')


# 生成邀请码
@app.route('/GenInvitationCode', methods=['GET', 'POST'])
@login_required
def GenInvitationCode():
    user_id = session.get('user_id')
    nowuser = User.query.filter(User.id == user_id).first()
    profile = Profile.query.filter(Profile.userid == user_id).first()
    assetname = redispool.hkeys('assets')
    followlist = redispool.hgetall('FollowList')
    photoname = redispool.hget('imagename', nowuser.email)
    if not photoname:
        photoname = 'springbird.jpg'
    code = str(uuid.uuid1())
    Code = InvitationCode(code=code)
    db.session.add(Code)
    db.session.commit()
    allcode = InvitationCode.query.order_by(InvitationCode.id.desc()).limit(10).all()
    return render_template('user-center.html', allcode=allcode, username=nowuser.username, profile=profile,
                           assetname=assetname, followlist=followlist, photoname=photoname)


# 取消漏洞关注
@app.route('/UnFollow')
@app.route('/UnFollow/<int:bugid>', methods=['GET', 'POST'])
@login_required
def UnFollow(bugid=None):
    if bugid:
        redispool.hdel('FollowList', bugid)
    return redirect(url_for('user'))


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
        elif not IsCode:
            flash("邀请码错误")
            return render_template('sign_up.html')
        else:
            user = User(email=email, username=username, password=password1)
            db.session.add(user)
            db.session.delete(IsCode)
            db.session.commit()
            return redirect(url_for('login'))


@app.route('/logout/')
@login_required
def logout():
    # session.pop('user_id')
    # del session('user_id')
    session.clear()
    return redirect(url_for('login'))


@app.route('/about/')
@login_required
def about():
    return render_template('about.html')


# 日志每页显示38条
@app.route('/log_detail/')
@app.route('/log_detail/<int:page>', methods=['GET'])
@login_required
def log_detail(page=None):
    bugbit, bugtype = core.GetBit()
    if not page:
        page = 1
    per_page = 38
    paginate = Log.query.order_by(Log.date.desc()).paginate(page, per_page, error_out=False)
    logs = paginate.items
    return render_template('log_detail.html', paginate=paginate, logs=logs, bugbit=bugbit, bugtype=bugtype)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


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


@app.route('/photo/', methods=['GET', 'POST'])
@login_required
def photo():
    user_id = session.get('user_id')
    nowuser = User.query.filter(User.id == user_id).first()
    photoname = redispool.hget('imagename', nowuser.email)
    if request.method == 'GET':
        return render_template('photo.html', photoname=photoname)
    else:
        img = request.files['photo']
        if img and core.allowed_file(img.filename):
            ext = img.filename.rsplit('.', 1)[1]
            email = nowuser.email
            photoname = email.split('@')[0] + "." + ext
            img.save(os.path.join(os.getcwd() + "/static/photo", photoname))
            redispool.hset('imagename', email, photoname)
            return redirect(url_for('user'))
        return '<p> 上传失败</p>'


@app.route('/domainName/<int:id>', methods=['GET'])
@app.route('/domainName/', methods=['GET'])
@login_required
def domainName(id=None):
    bugbit, bugtype = core.GetBit()
    if not id:
        id = 1
    per_page = 10
    paginate = BaseInfo.query.order_by(BaseInfo.date.desc()).filter(BaseInfo.boolcheck == 0).paginate(id, per_page, error_out=False)
    infos = paginate.items
    return render_template('domainName.html', paginate=paginate, infos=infos, bugbit=bugbit, bugtype=bugtype)


@app.route('/IP/<int:id>', methods=['GET'])
@app.route('/IP/', methods=['GET'])
@login_required
def IP(id=None):
    bugbit, bugtype = core.GetBit()
    if not id:
        id = 1
    per_page = 10
    paginate = BaseInfo.query.order_by(BaseInfo.date.desc()).filter(BaseInfo.boolcheck == 1).paginate(id, per_page, error_out=False)
    infos = paginate.items
    return render_template('IP.html', paginate=paginate, infos=infos, bugbit=bugbit, bugtype=bugtype)



@app.route('/seriousBug/<int:page>', methods=['GET'])
@app.route('/seriousBug')
@login_required
def seriousBug(page=None):
    bugbit, bugtype = core.GetBit()
    if not page:
        page = 1
    per_page = 10
    paginate = BugList.query.order_by(BugList.id.desc()).filter(BugList.buggrade == "Serious").paginate(page, per_page, error_out=False)
    seriousbug = paginate.items
    return render_template('bug-list.html', paginate=paginate, bugs=seriousbug, bugbit=bugbit, bugtype=bugtype)


@app.route('/leaks/<int:page>', methods=['GET'])
@app.route('/leaks')
@login_required
def FileLeakBug(page=None):
    bugbit, bugtype = core.GetBit()
    if not page:
        page = 1
    per_page = 10
    paginate = BugList.query.order_by(BugList.id.desc()).paginate(page, per_page, error_out=False)
    # bugs = paginate.items
    leak = []
    leaks = BugList.query.filter()
    for bug in leaks:
        if "文件泄露" in bug.bugname:
            leak.append(bug)
    return render_template('bug-list.html', paginate=paginate, bugs=leak, bugbit=bugbit, bugtype=bugtype)


if __name__ == '__main__':
    app.run()
