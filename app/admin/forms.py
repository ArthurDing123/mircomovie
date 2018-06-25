#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author:Arthur

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField, TextAreaField,SelectMultipleField

from wtforms.validators import DataRequired, EqualTo, Email, Length, ValidationError
from flask_wtf.file import FileField, FileAllowed
from app.models import Admin, Tag, Auth,Role,Movie
from flask import session


class LoginForm(FlaskForm):
    """
    登录表单
    """
    username = StringField('用户名', validators=[DataRequired("用户名不能为空"),
                                              Length(2, 20, message="用户名长度为2-20位"),
                                              ])
    password = PasswordField('密码', validators=[DataRequired("密码不能为空"),
                                               Length(6, 18, message="密码长度为6-18为")])
    submit = SubmitField('登录')

    # 验证用户是否存在
    def validate_username(self, username):
        admin = Admin.query.filter_by(username=username.data).first()
        if admin is None:
            raise ValidationError("账号不存在")


class TagForm(FlaskForm):
    """
    标签
    """
    name = StringField('标签名称', validators=[DataRequired("请输入内容")])
    submit = SubmitField('添加')

    def validate_name(self, field):
        tag = Tag.query.filter_by(name=field.data).count()
        if tag != 0:
            raise ValidationError("标签已存在")


class MovieForm(FlaskForm):
    """
    电影表单
    """
    tags = Tag.query.all()
    title = StringField("片名", validators=[DataRequired("请输入内容")])
    url = FileField("文件", validators=[FileAllowed(['mp4', '3gp', 'rmvb', 'rm'], message="不支持该格式")])
    info = TextAreaField("介绍", validators=[DataRequired("请输入内容")])
    logo = FileField("封面", validators=[FileAllowed(['jpg', 'png', 'jpeg'], message="不支持该格式")])
    star = SelectField("星级", coerce=int, choices=[(1, "1星"), (2, "2星"), (3, "3星"), (4, "4星"), (5, "5星"), ])
    tag_id = SelectField("标签", coerce=int, choices=[(t.id, t.name) for t in tags])
    area = StringField("地区", validators=[DataRequired("请输入内容")])
    lenth = StringField("片长", validators=[DataRequired("请输入内容")])
    release_time = DateField("上映时间", validators=[DataRequired("请选择时间")])

    submit = SubmitField("添加")

    def validate_title(self,field):
        movie = Movie.query.filter_by(title=field.data).count()
        if movie != 0:
            raise ValidationError("电影标题已存在")

class PreviewForm(FlaskForm):
    """
    预告
    """
    title = StringField("预告标题", validators=[DataRequired("请输入内容")])
    logo = FileField("预告封面", validators=[FileAllowed(['jpg', 'png', 'jpeg'], message="不支持该格式")])

    submit = SubmitField()


class PwdForm(FlaskForm):
    """
    修改密码表单
    """
    old_pwd = PasswordField("旧密码", validators=[DataRequired("密码不能为空"), Length(6, 20, message="密码长度为6-20")])
    new_pwd = PasswordField("新密码", validators=[DataRequired("密码不能为空"), Length(6, 20, message="密码长度为6-20")])
    new_pwd2 = PasswordField("再次输入新密码", validators=[EqualTo('new_pwd', message="两次输入不一致")])

    submit = SubmitField()

    def validate_old_pwd(self, field):
        username = session['admin']
        admin = Admin.query.filter_by(username=username).first()
        if not admin.check_password(field.data):
            raise ValidationError("您输入的旧密码有误")


class AuthForm(FlaskForm):
    """
    权限表单
    """
    name = StringField("权限名称", validators=[DataRequired("权限名称不能为空")])
    url = StringField("权限地址", validators=[DataRequired("权限地址不能为空")])

    submit = SubmitField()

    def validate_name(self, field):
        auth = Auth.query.filter_by(name=field.data).count()
        if auth != 0:
            raise ValidationError("权限名称已存在")

class RoleForm(FlaskForm):
    """
    角色表
    """
    auths = Auth.query.all()
    name = StringField("角色名称",validators=[DataRequired("请输入名称")])
    auths = SelectMultipleField("操作权限",coerce=int, choices=[(v.id,v.name) for v in auths])

    submit = SubmitField()

    #验证角色名称，确保新添加的名称不在库内
    def validate_name(self,field):
        role = Role.query.filter_by(name=field.data).count()
        if role != 0:
            raise ValidationError("角色名称已存在")


class AdminForm(FlaskForm):
    """
    管理员表
    """
    role = Role.query.all()

    name = StringField("管理员名称",validators=[DataRequired("管理员密码不能为空")])
    pwd = PasswordField("管理员密码", validators=[DataRequired("密码不能为空"), Length(6, 20, message="密码长度为6-20")])
    pwd2 = PasswordField("重复密码", validators=[EqualTo('pwd', message="两次输入不一致")])
    roles = SelectField("所属角色",validators=[DataRequired("所属角色不能为空")], coerce=int,choices=[(v.id, v.name) for v in role])

    submit = SubmitField()

    #验证要添加的管理员是否已经存在
    def validate_name(self,field):
        admin = Admin.query.filter_by(username=field.data).count()
        if admin != 0:
            raise ValidationError("管理员已存在")
