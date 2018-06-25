#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author:Arthur

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(db.Model):
    """
    用户表
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True)  # 用户名
    password = db.Column(db.String(100))  # 密码
    email = db.Column(db.String(100), unique=True)  # 邮箱
    phone_num = db.Column(db.String(11), unique=True)  # 电话号码
    info = db.Column(db.Text)  # 用户信息
    avatar = db.Column(db.String(255))  # 头像
    addtime = db.Column(db.DateTime, default=datetime.utcnow())  # 注册时间
    uuid = db.Column(db.String(255), unique=True)  # 唯一标识符uuid
    userlogs = db.relationship('UserLog', backref='user')  # 会员日志外键
    comments = db.relationship('Comment', backref='user')  # 评论数
    moviecols = db.relationship('Moviecol', backref='user')  # 电影收藏

    # password　　has加密
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # password  has验证
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.username


class UserLog(db.Model):
    """
    会员日志表
    """
    __tablename__ = 'userlog'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(100))  # 登录ip
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 会员外键
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 日志时间

    def __repr__(self):
        return '<UserLog %r>' % self.id


class Admin(db.Model):
    """
    管理员表
    """
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True)  # 用户名
    password = db.Column(db.String(100), unique=True)  # 密码
    is_super = db.Column(db.SmallInteger)  # 是否为超级管理员 0是
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # 所属角色
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    adminlogs = db.relationship("AdminLog", backref='admin')
    oplogs = db.relationship("Oplog", backref='admin')

    # hash加密
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # hash解密
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<Admin %r>' % self.username


class AdminLog(db.Model):
    """
    管理员日志
    """
    __tablename__ = 'adminlog'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(100))  # 登录ip
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 会员外键
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 日志时间

    def __repr__(self):
        return '<AdminLog %r>' % self.id


class Oplog(db.Model):
    """
    管理员操作日志
    """
    __tablename__ = 'oplog'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(100))  # 登录ip
    opreason = db.Column(db.String(255))  # 操作原因
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 会员外键
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 日志时间

    def __repr__(self):
        return '<AdminLog %r>' % self.id


class Tag(db.Model):
    """
    标签表
    """
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24))  # 标签名称
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 日志时间
    movies = db.relationship("Movie", backref='tag')  # 电影关联

    def __repr__(self):
        return '<Tag %r>' % self.id


class Movie(db.Model):
    """
    电影表
    """
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)  # 标题
    url = db.Column(db.String(255), unique=True)  # 地址
    info = db.Column(db.Text)  # 简介
    logo = db.Column(db.String(255))  # 封面
    star = db.Column(db.SmallInteger)  # 星级
    playnum = db.Column(db.BigInteger)  # 播放量
    commentnum = db.Column(db.BigInteger)  # 评论数
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))  # 所属标签，
    area = db.Column(db.String(255))  # 上映地区
    release_time = db.Column(db.Date)  # ＃上映时间
    length = db.Column(db.String(100))  # 播放时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    comments = db.relationship('Comment', backref='movie')  # 电影的评论
    moviecols = db.relationship('Moviecol', backref='movie')  # 电影收藏

    def __repr__(self):
        return '<Movie %r>' % self.title


class Preview(db.Model):
    """
    上映预告表
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)  # 标题
    logo = db.Column(db.String(255))  # 封面
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return '<Preview %r>' % self.title


class Comment(db.Model):
    """
    评论表
    """
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)  # 评论内容
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 评论时间

    def __repr__(self):
        return '<Comment %r>' % self.id


class Moviecol(db.Model):
    """
    电影收藏
    """
    __tablename__ = "moviecol"
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 评论时间

    def __repr__(self):
        return '<Moviecol %r>' % self.id


class Role(db.Model):
    """
    角色管理
    """
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)  # 名称
    auths = db.Column(db.String(100))  # 角色权限列表
    admins = db.relationship("Admin", backref='role')  # 会员外键
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 时间

    def __repr__(self):
        return '<Role %r>' % self.name


class Auth(db.Model):
    """
    权限表单
    """
    __tablename__ = 'auth'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)  # 权限名称
    url = db.Column(db.String(32))  # 权限地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 评论时间

    def __repr__(self):
        return '<Auth %r>' % self.name
