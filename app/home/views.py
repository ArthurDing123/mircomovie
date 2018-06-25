#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author:Arthur

import os
from flask import render_template, redirect, flash, request, url_for, session
from uuid import uuid4
from werkzeug.utils import secure_filename
from tools import change_upload_filename
import json
from app import app, db
from app.home import home
from .forms import LoginForm, RegisterForm, UserForm, PwdForm, CommentForm
from app.models import User, UserLog, Preview, Tag, Movie, Comment, Moviecol
from tools import user_login_req


# 主页
@home.route('/', methods=["GET"])
def index():
    tags = Tag.query.all()
    page_data = Movie.query

    # 标签
    tid = request.args.get('tid', 0)
    if int(tid) != 0:
        page_data = page_data.filter_by(tag_id=int(tid))
    # 星级
    star = request.args.get('star', 0)
    if int(star) != 0:
        page_data = page_data.filter_by(star=int(star))
    # 上映时间
    time = request.args.get('time', 0)
    if int(time) != 0:
        if int(time) == 1:
            page_data = page_data.order_by(Movie.addtime.desc())
        else:
            page_data = page_data.order_by(Movie.addtime.asc())
    # 播放量
    pm = request.args.get('pm', 0)
    if int(pm) != 0:
        if int(pm) == 1:
            page_data = page_data.order_by(Movie.playnum.desc())
        else:
            page_data = page_data.order_by(Movie.playnum.asc())
    # 评论量
    cm = request.args.get('cm', 0)
    if int(cm) != 0:
        if int(cm) == 1:
            page_data = page_data.order_by(Movie.commentnum.desc())
        else:
            page_data = page_data.order_by(Movie.commentnum.asc())

    page = int(request.args.get('page', 1))
    page_data = page_data.paginate(page, 10)
    p = {
        "tid": tid,
        "star": star,
        "time": time,
        "cm": cm,
        "pm": pm,
        "page": page,

    }

    return render_template('home/index.html', tags=tags, p=p, page_data=page_data)


# 评论
@home.route('/search')
@home.route('/search/<int:page>')
def search(page=None):
    if page is None:
        page = 1
    key = request.args.get('key')
    page_data = Movie.query
    page_data = page_data.filter(Movie.title.ilike("%" + key + "%"))
    page_data = page_data.filter(Movie.info.ilike("%" + key + "%")).paginate(page,10)
    return render_template('home/search.html', key=key,page_data=page_data)


# 评论
@home.route('/comments')
@home.route('/comments/<int:page>')
@user_login_req
def comments(page=None):
    if page == None:
        page = 1
    user = User.query.filter_by(username=session.get('user')).first()
    page_data = Comment.query.filter_by(user_id=user.id).paginate(page, 10)

    return render_template('home/comments.html', user=user, page_data=page_data)


# 登录日志
@home.route('/loginlog/<int:page>')
def loginlog(page):
    page_data = UserLog.query.filter_by(user_id=int(session.get('User_id'))).order_by(UserLog.addtime).paginate(page, 10)

    return render_template('home/loginlog.html', page_data=page_data)


# 添加电影收藏
@home.route('/moviecol/add')
def moviecol_add():
    uid = int(request.args.get('uid', ""))
    mid = int(request.args.get("mid", ""))
    moviecol = Moviecol.query.filter_by(
        user_id=int(uid),
        movie_id=int(mid)
    ).count()
    if moviecol == 0:
        m = Moviecol(user_id=uid, movie_id=mid)
        db.session.add(m)
        db.session.commit()
        data = dict(ok=1)
    else:
        data = dict(ok=0)
    return json.dumps(data)


# 收藏电影
@home.route('/moviecol')
@home.route('/moviecol/<int:page>')
def moviecol(page=None):
    if page is None:
        page = 1
    page_data = Moviecol.query.filter_by(user_id=int(session.get('User_id'))).join(Movie).join(User).filter(
        Moviecol.movie_id == Movie.id,
        Moviecol.user_id == User.id
    ).order_by(Moviecol.addtime.desc()).paginate(page, 10)

    return render_template('home/moviecol.html', page_data=page_data)

#播放页
@home.route('/play/<int:id>')
@home.route('/play/<int:id>/<int:page>', methods=["get", "post"])
def play(id=None, page=None):
    if page == None:
        page = 1
    movie = Movie.query.get_or_404(id)
    movie.playnum += 1
    form = CommentForm()
    # 评论
    if session.get('user') and form.validate_on_submit():
        data = form.data
        comm = Comment(content=data['content'],
                       user_id=session.get('User_id'),
                       movie_id=movie.id)
        db.session.add(comm)
        db.session.commit()
        movie.commentnum += 1
        db.session.add(movie)
        db.session.commit()
        flash("评论成功", "ok")
        return redirect(url_for('home.play', id=movie.id, page=1))
    db.session.add(movie)
    db.session.commit()
    # 评论列表

    page_data = Comment.query.join(User).filter(User.id == Comment.user_id).order_by(Comment.addtime.desc()).paginate(
        page, 10)
    return render_template('home/play.html', movie=movie, form=form, page_data=page_data, page=page)


# 登录
@home.route('/login', methods=['get', 'post'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(username=data['username']).first()
        if user.check_password(data['password']):
            session['user'] = user.username
            session['User_id'] = user.id
            # 持久化　默认保存31天，可通过在config中设置PERMENENT_SESSION_LIFETIME改变
            session.permanent = True
            userlog = UserLog(
                ip=request.remote_addr,
                user_id=user.id,
            )
            db.session.add(userlog)
            db.session.commit()

            return redirect(url_for('home.index'))
        else:
            flash("密码错误", "err")
    return render_template('home/login.html', form=form)


# 注册
@home.route('/register', methods=['get', 'post'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            username=data['username'],
            email=data['email'],
            phone_num=data['phone_num'],
            uuid=uuid4().hex
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        flash("注册成功", 'ok')
        return redirect(url_for('home.login'))

    return render_template('home/register.html', form=form)


# 退出
@home.route('/logout')
def logout():
    # 删除session
    session.clear()
    return redirect(url_for('home.login'))


# 会员
@home.route('/user', methods=['get', 'post'])
@user_login_req
def user():
    form = UserForm()
    user = User.query.get_or_404(session.get('User_id'))
    if request.method == 'GET':
        form.info.data = user.info
    if form.validate_on_submit():
        data = form.data
        if user.username != data['username']:
            c = User.query.filter_by(username=data['username']).count()
            if c != 0:
                flash("用户名已存在", "err")
                return redirect(url_for('home.user'))
            user.username = data['username']
        if user.email != data['email']:
            c = User.query.filter_by(email=data['email']).count()
            if c != 0:
                flash("邮箱已存在", "err")
                return redirect(url_for('home.user'))
            user.email = data['email']
        if user.phone_num != data['phone_num']:
            c = User.query.filter_by(phone_num=data['phone_num']).count()
            if c != 0:
                flash("手机号已存在", "err")
                return redirect(url_for('home.user'))
            user.phone_num = data['phone_num']
        if data['avatar']:
            if user.avatar:
                os.remove(os.path.join(app.config['UP_AVATAR_DIR'], user.avatar))
            file = secure_filename(form.avatar.data.filename)
            avatar = change_upload_filename(file)
            form.avatar.data.save(os.path.join(app.config['UP_AVATAR_DIR'], avatar))
            user.avatar = avatar

        user.info = data['info']
        db.session.add(user)
        db.session.commit()
        flash("保存成功", "ok")
        return redirect(url_for('home.user'))
    return render_template('home/user.html', form=form, user=user)


# 修改密码
@user_login_req
@home.route('/pwd', methods=['get', 'post'])
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=session.get('user')).first()
        user.set_password(form.pwd.data)
        db.session.add(user)
        db.session.commit()
        flash("密码修改成功", 'ok')
    return render_template('home/pwd.html', form=form)


@home.route('/animation')
def animation():
    preview = Preview.query.all()

    return render_template('home/animation.html', preview=preview)
