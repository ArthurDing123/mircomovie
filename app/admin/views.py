#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author:Arthur

import os
from flask import render_template, redirect, flash, request, url_for, session
from werkzeug.utils import secure_filename
from app.admin import admin
from app.admin.forms import LoginForm,AdminForm,AuthForm,TagForm,MovieForm,PreviewForm,RoleForm
from app.models import Tag,Movie,Preview,Moviecol,Auth,Role,Admin,User,Comment
from app import db, app
from tools import change_upload_filename, admin_login_req,admin_auth


# 主页
@admin.route('/')
@admin.route('/index')
@admin_login_req
def index():
    return render_template('admin/index.html')


# 添加标签
@admin.route('/tag_add', methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        name = form.name.data
        tag = Tag.query.filter_by(name=name).count()
        if tag == 0:
            db.session.add(Tag(name=name))
            db.session.commit()
            flash("标签添加成功", category='ok')
            return redirect(url_for('admin.tag_add'))
        flash("该标签已经存在", category='err')
        return redirect(url_for("admin.tag_add"))

    return render_template('admin/tag_add.html', form=form)


# 标签列表
@admin.route('/tag_list/<page>')
@admin_login_req
@admin_auth
def tag_list(page):
    page_data = Tag.query.order_by(Tag.addtime.desc()).paginate(int(page), 10)
    return render_template('admin/tag_list.html', page_data=page_data)


# 删除标签
@admin.route('/tag_del/<id>')
@admin_login_req
@admin_auth
def tag_del(id):
    tag = Tag.query.filter_by(id=int(id)).first_or_404()
    if tag:
        db.session.delete(tag)
        db.session.commit()
        flash("删除成功", "ok")
        return redirect(url_for('admin.tag_list', page=1))


# 编辑标签
@admin.route('/tag/edit/<id>', methods=['get', 'post'])
@admin_login_req
@admin_auth
def tag_edit(id):
    form = TagForm()
    tag = Tag.query.get_or_404(int(id))  # 修改前的tag
    if form.validate_on_submit():
        t = Tag.query.filter_by(name=form.name.data).count()  # 新的name在数据库中的数量
        if tag.name != form.name.data and t == 0:
            tag.name = form.name.data
            db.session.add(tag)
            db.session.commit()
            flash("标签修改成功", "ok")
            return redirect(url_for('admin.tag_edit', id=tag.id))
        flash("标签修改失败", 'err')
        return redirect(url_for('admin.tag_edit', id=tag.id))
    return render_template('admin/tag_edit.html', form=form, tag=tag)


# 添加电影
@admin.route('/movie_add', methods=['get', 'post'])
@admin_login_req
@admin_auth
def movie_add():
    form = MovieForm()
    if form.validate_on_submit():
        file_url = secure_filename(form.url.data.filename)
        file_logo = secure_filename(form.logo.data.filename)
        url = change_upload_filename(file_url)
        logo = change_upload_filename(file_logo)
        form.url.data.save(os.path.join(app.config['UP_MOVIE_DIR'], url))
        form.logo.data.save(os.path.join(app.config['UP_PIC_DIR'], logo))
        movie = Movie(
            title=form.title.data,
            url=url,
            info=form.info.data,
            logo=logo,
            star=int(form.star.data),
            playnum=0,
            commentnum=0,
            tag_id=int(form.tag_id.data),
            area=form.area.data,
            length=form.lenth.data,
            release_time=form.release_time.data,

        )
        db.session.add(movie)
        db.session.commit()
        flash("添加成功", "ok")
    return render_template('admin/movie_add.html', form=form)


# 电影列表
@admin.route('/movie_list/<page>')
@admin_login_req
@admin_auth
def movie_list(page):
    page_data = Movie.query.join(Tag).filter(Tag.id == Movie.tag_id).order_by(Movie.addtime.desc()).paginate(int(page),
                                                                                                             10)

    return render_template('admin/movie_list.html', page_data=page_data)


# 删除电影
@admin.route('/movie/del/<id>')
@admin_login_req
@admin_auth
def movie_del(id):
    movie = Movie.query.get_or_404(int(id))
    try:
        os.remove(os.path.join(app.config['UP_MOVIE_DIR'], movie.url))
        os.remove(os.path.join(app.config['UP_PIC_DIR'], movie.logo))
    except:
        pass
    db.session.delete(movie)
    db.session.commit()
    flash("删除成功", "ok")
    return redirect(url_for('admin.movie_list', page=1))


# 编辑电影
@admin.route('/movie/edit/<id>', methods=['get', 'post'])
@admin_login_req
@admin_auth
def movie_edit(id):
    form = MovieForm()
    movie = Movie.query.get_or_404(int(id))  # 修改前的tag
    # 由于有些前段的html标签没有value属性，不是直接渲染，所以需要后台添加数据到前端
    if request.method == "GET":
        form.tag_id.data = movie.tag_id
        form.star.data = movie.star
        form.info.data = movie.info
    if form.validate_on_submit():
        data = form.data
        t = Movie.query.filter_by(title=form.title.data).count()  # 新的name在数据库中的数量
        # 传进来的title和原来的title不一样并且库里面没有刚刚传进来的title，这时候更新操作
        if t == 0:
            movie.title = data['title']
            movie.info = data['info']
            movie.star = int(data['star']),
            movie.tag_id = int(data['tag_id']),
            movie.area = data['area'],
            movie.lenth = data['lenth'],
            movie.release_time = data['release_time'],
            # 有新url提交说明有新数据要上传
            if form.url.data is not None:
                try:
                    os.remove(os.path.join(app.config['UP_MOVIE_DIR'], movie.url))
                except:
                    pass
                file_url = secure_filename(form.url.data.filename)
                url = change_upload_filename(file_url)
                movie.url = url
                form.url.data.save(os.path.join(app.config['UP_MOVIE_DIR'], url))

            # 有新logo提交说明有新数据要上传
            if form.logo.data is not None:
                try:
                    os.remove(os.path.join(app.config['UP_PIC_DIR'], movie.logo))
                except:
                    pass
                file_logo = secure_filename(form.url.data.filename)
                logo = change_upload_filename(file_logo)
                movie.logo = logo
                form.url.data.save(os.path.join(app.config['UP_PIC_DIR'], logo))

            db.session.add(movie)
            db.session.commit()
            flash("标签修改成功", "ok")
            return redirect(url_for('admin.movie_edit', id=movie.id))
        flash("标题已存在", 'err')
        return redirect(url_for('admin.movie_edit', id=movie.id))
    return render_template('admin/movie_edit.html', form=form, movie=movie)


# 添加预告
@admin.route('/preview/add', methods=['get', 'post'])
@admin_login_req
@admin_auth
def preview_add():
    form = PreviewForm()
    if form.validate_on_submit():
        title = form.title.data
        t = Preview.query.filter_by(title=title).count()
        if t == 0:
            file = secure_filename(form.logo.data.filename)
            logo = change_upload_filename(file)
            form.logo.data.save(os.path.join(app.config['UP_PIC_DIR'], logo))
            preview = Preview(title=title, logo=logo)
            db.session.add(preview)
            db.session.commit()
            flash("添加成功", 'ok')
        else:
            flash("标题已存在", "err")
    return render_template('admin/preview_add.html', form=form)


# 预告列表
@admin.route('/preview/list/<page>')
@admin_login_req
@admin_auth
def preview_list(page):
    page_data = Preview.query.order_by(Preview.addtime.desc()).paginate(int(page), 2)

    return render_template('admin/preview_list.html', page_data=page_data)


# 删除预告
@admin.route('/preview/del/<id>')
@admin_login_req
@admin_auth
def preview_del(id):
    preview = Preview.query.get_or_404(int(id))
    try:
        os.remove(os.path.join(app.config['UP_PIC_DIR'], preview.logo))
    except:
        pass
    db.session.delete(preview)
    db.session.commit()
    flash("删除成功", "ok")
    return redirect(url_for('admin.preview_list', page=1))


# 编辑预告
@admin.route('/preview/edit/<id>', methods=['get', 'post'])
@admin_login_req
@admin_auth
def preview_edit(id):
    form = PreviewForm()
    preview = Preview.query.get_or_404(int(id))
    if request.method == 'psot':
        form.logo.data = preview.logo
    if form.validate_on_submit():
        title = form.title.data
        t = Preview.query.filter_by(title=title).count()
        if t == 0:
            preview.title = form.title.data
            if form.logo.data is not None:
                try:
                    os.remove(os.path.join(app.config['UP_PIC_DIR'], preview.logo))
                except:
                    pass
                file = secure_filename(form.logo.data.filename)
                logo = change_upload_filename(file)
                form.logo.data.save(os.path.join(app.config['UP_PIC_DIR'], logo))
                preview.logo = logo
            db.session.add(preview)
            db.session.commit()
            flash("修改成功", 'ok')
        else:
            flash("标题已存在", "err")
    return render_template('admin/preview_edit.html', form=form, preview=preview)


# 会员列表
@admin.route('/user/list/<int:page>')
@admin_login_req
@admin_auth
def user_list(page):
    page_data = User.query.paginate(page, 10)
    return render_template('admin/user_list.html', page_data=page_data)


# 查看会员
@admin.route('/user/view/<int:id>')
@admin_login_req
@admin_auth
def user_view(id):
    user_info = User.query.get_or_404(id)
    return render_template('admin/user_view.html', user_info=user_info)


# 删除会员
@admin.route('/user/del/<int:id>')
@admin_login_req
@admin_auth
def user_del(id):
    user = User.query.get_or_404(int(id))
    try:
        os.remove(os.path.join(app.config['UP_AVATAR_DIR'], user.avatar))
    except:
        pass
    db.session.delete(user)
    db.session.commit()
    flash("删除成功", "ok")
    return redirect(url_for('admin.user_list', page=1))


# 评论列表
@admin.route('/comment/list')
@admin.route('/comment/list/<int:page>')
@admin_login_req
@admin_auth
def comment_list(page=None):
    if page == None:
        page = 1
    page_data = Comment.query.join(Movie).join(User).filter(
        Movie.id == Comment.movie_id, User.id == Comment.user_id
    ).paginate(page, 10)

    return render_template('admin/comment_list.html', page_data=page_data)


# 删除评论
@admin.route('comment/del/<int:id>')
@admin_login_req
@admin_auth
def comment_del(id):
    comment = Comment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    flash("删除成功", "ok")
    return redirect(url_for('admin.comment_list', page=1))


# 收藏列表
@admin.route('/moviecol/list/<int:page>')
@admin_login_req
@admin_auth
def moviecol_list(page):
    page_data = Moviecol.query.join(Movie).join(User).filter(
        Movie.id == Moviecol.movie_id, User.id == Moviecol.user_id
    ).paginate(page, 10)

    return render_template('admin/moviecol_list.html', page_data=page_data)


# 操作日志列表
@admin.route('/oplog/list')
@admin_login_req
@admin_auth
def oplog_list():
    return render_template('admin/oplog_list.html')


# 管理员登录日志列表
@admin.route('/adminloginlog/list')
@admin_login_req
@admin_auth
def adminloginlog_list():
    return render_template('admin/adminloginlog_list.html')


# 会员登录日志列表
@admin.route('/userloginlog/list')
@admin_login_req
@admin_auth
def userloginlog_list():
    return render_template('admin/userloginlog_list.html')


# 添加权限
@admin.route('/auth/add', methods=['get', 'post'])
@admin_login_req
@admin_auth
def auth_add():
    form = AuthForm()
    if form.validate_on_submit():
        auth = Auth(name=form.name.data,
                    url=form.url.data)
        db.session.add(auth)
        db.session.commit()
        flash("标签添加成功", "ok")
        return redirect(url_for("admin.auth_add"))
    return render_template('admin/auth_add.html', form=form)


# 权限列表
@admin.route('/auth/list/<int:page>')
@admin_login_req
@admin_auth
def auth_list(page):
    page_data = Auth.query.order_by(Auth.addtime.desc()).paginate(page, 10)
    return render_template('admin/auth_list.html', page_data=page_data)


# 删除权限
@admin.route('/auth/del/<int:id>')
@admin_login_req
@admin_auth
def auth_del(id):
    auth = Auth.query.get_or_404(id)
    db.session.delete(auth)
    db.session.commit()
    flash("删除成功", "ok")
    return redirect(url_for('admin.auth_list', page=1))


# 编辑权限
@admin.route('/auth/edit/<int:id>', methods=['get', 'post'])
@admin_login_req
@admin_auth
def auth_edit(id):
    auth = Auth.query.get_or_404(id)
    form = AuthForm()
    if form.validate_on_submit():
        auth.name = form.name.data
        auth.url = form.url.data
        db.session.add(auth)
        db.session.commit()
        flash("权限修改成功", "ok")
    return render_template('admin/auth_edit.html', form=form, auth=auth)


# 添加角色
@admin.route('/role/add', methods=['get', 'post'])
@admin_login_req
@admin_auth
def role_add():
    form = RoleForm()
    if form.validate_on_submit():
        role = Role(
            name=form.name.data,
            auths=','.join(map(lambda v: str(v), form.auths.data))
        )
        db.session.add(role)
        db.session.commit()
        flash("角色添加成功", 'ok')
        return redirect(url_for('admin.role_add'))
    return render_template('admin/role_add.html', form=form)


# 角色列表
@admin.route('/role/list/<int:page>')
@admin_login_req
@admin_auth
def role_list(page):
    page_data = Role.query.order_by(Role.addtime.desc()).paginate(page,10)

    return render_template('admin/role_list.html',page_data=page_data)

# 删除角色
@admin.route('/role/del/<int:id>')
@admin_login_req
@admin_auth
def role_del(id):
    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash("角色删除成功", 'ok')
    return redirect(url_for('admin.role_list',page=1))


# 添加角色
@admin.route('/role/edit/<int:id>', methods=['get', 'post'])
@admin_login_req
@admin_auth
def role_edit(id):
    form = RoleForm()
    role = Role.query.get_or_404(id)
    if request.method == "GET":
        form.auths.data = list(map(lambda v:int(v), role.auths.split(',')))
    if form.validate_on_submit():
        role.name = form.name.data,
        role.auths = ','.join(map(lambda v: str(v), form.auths.data))
        db.session.add(role)
        db.session.commit()
        flash("角色编辑成功", 'ok')
        return redirect(url_for('admin.role_edit'))
    return render_template('admin/role_edit.html', form=form,role=role)

# 添加管理员
@admin.route('/admin/add',methods=['get','post'])
@admin_login_req
@admin_auth
def admin_add():
    form = AdminForm()
    if form.validate_on_submit():
        admin = Admin(username = form.name.data,
                      role_id = int(form.roles.data),
                      is_super= 1

        )
        admin.set_password(form.pwd.data)
        db.session.add(admin)
        db.session.commit()
        flash("添加成功","ok")
        return redirect(url_for('admin.admin_add'))
    return render_template('admin/admin_add.html', form=form)


# 管理员列表
@admin.route('/admin/list/<int:page>')
@admin_login_req
@admin_auth
def admin_list(page):
    page_data = Admin.query.join(Role).filter(Role.id==Admin.role_id).paginate(page,10)
    return render_template('admin/admin_list.html',page_data=page_data)


# 登录
@admin.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first_or_404()
        if admin and admin.check_password(form.password.data):
            session['admin'] = admin.username
            session['admin_id'] = admin.id
            return redirect(url_for('admin.index'))
        flash("密码错误")
        print(request.url)
        return redirect(url_for('admin.login'))
    return render_template('admin/login.html', form=form)


# 修改密码
@admin.route('/pwd', methods=['GET', 'POST'])
@admin_login_req
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        username = session['admin']
        admin = Admin.query.filter_by(username=username).first_or_404()
        admin.set_password(form.new_pwd.data)
        if admin.password:
            db.session.add(admin)
            db.session.commit()
            flash("修改成功", "ok")
        else:
            flash("新密码处理失败", "err")
        return redirect(url_for('admin.pwd'))

    return render_template('admin/pwd.html', form=form)


# 退出
@admin.route('/logout', methods=['GET', 'POST'])
@admin_login_req
def logout():
    session.pop("admin", None)
    return redirect(url_for('admin.login'))
