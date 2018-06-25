#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author:Arthur

from flask_wtf import FlaskForm
from flask import session
from wtforms import StringField, PasswordField, SubmitField,TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email, Length, ValidationError
from flask_wtf.file import FileField,FileAllowed
from app.models import User


class LoginForm(FlaskForm):
    """
    登录表单
    """
    username = StringField('账号', validators=[DataRequired("用户名不能为空"),
                                             Length(2, 20, message="用户名长度为2-20位"),

                                             ])

    password = PasswordField('密码', validators=[DataRequired("密码不能为空"),
                                               Length(6, 18, message="密码长度为6-18为")])

    submit = SubmitField()

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if not user:
            raise ValidationError("用户名不存在")


class RegisterForm(FlaskForm):
    """
    注册表单
    """
    username = StringField('用户名', validators=[DataRequired("用户名不能为空"),
                                              Length(2, 20, message="用户名长度为2-20位"),

                                              ])
    email = StringField('邮箱', validators=[DataRequired("邮箱不能为空"), Email("邮箱格式不正确")])
    password = PasswordField('密码', validators=[DataRequired("密码不能为空"),
                                               Length(6, 18, message="密码长度为6-18为")])
    password2 = PasswordField('密码', validators=[EqualTo('password', message="两次输入的密码不一致")])

    phone_num = StringField("手机", validators=[Length(11, 11, message="手机号码需11位数字")])
    submit = SubmitField('登录')

    def validate_username(self, flied):
        user = User.query.filter_by(username=flied.data).count()
        if user != 0:
            raise ValidationError("用户名已存在")

    def validate_email(self, flied):
        email = User.query.filter_by(email=flied.data).count()
        if email != 0:
            raise ValidationError("邮箱已存在已存在")

    def validate_phone_num(self, flied):
        phone_num = User.query.filter_by(phone_num=flied.data).count()
        if phone_num != 0:
            raise ValidationError("号码已存在")

class UserForm(FlaskForm):
    """
    会员表单
    """
    username = StringField("用户",validators=[DataRequired("用户不能为空")])
    email = StringField("邮箱",validators=[Email("邮箱格式不正确")])
    phone_num = StringField("手机",validators=[Length(11,11,message="号码长度为11位")])
    avatar = FileField("头像",validators=[FileAllowed(['jpg','jpeg','png'],message="该格式不支持")])
    info = TextAreaField("简介")
    submit = SubmitField()

class PwdForm(FlaskForm):
    """
    修改密码表单
    """
    old_pwd = PasswordField('旧密码', validators=[DataRequired("密码不能为空"),
                                               Length(6, 18, message="密码长度为6-18为")])
    pwd = PasswordField('新密码', validators=[DataRequired("密码不能为空"),
                                               Length(6, 18, message="密码长度为6-18为")])
    pwd2 = PasswordField('重复密码', validators=[EqualTo('pwd',message="两次输入的密码不一致")])

    submit = SubmitField()

    def validate_old_pwd(self,field):
        user = User.query.filter_by(username=session.get('user')).first()
        if not user.check_password(field.data):
            raise ValidationError("原密码有误")



class CommentForm(FlaskForm):
    """
    评论表单
    """
    content = TextAreaField("内容", validators=[DataRequired("评论不能为空")])
    submit = SubmitField()