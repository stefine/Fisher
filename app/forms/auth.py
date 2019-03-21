#!/usr/bin/python
# -*- coding:utf-8 -*-


from wtforms import Form, StringField, PasswordField
from wtforms.validators import Length, DataRequired, Email, ValidationError, EqualTo

from app.models.user import User


class RegisterForm(Form):
    email = StringField(validators=[DataRequired(),
                                    Length(min=8, max=64),
                                    Email(message="电子邮箱不符合规定")])
    password = PasswordField(validators=[DataRequired(message="密码不为空, 请输入密码"),
                                         Length(min=6, max=32)])
    nickname = StringField(validators=[DataRequired(),
                                       Length(2, 10, message="昵称不少于两个字符")])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("电子邮箱已经存在")

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError("名字已经存在")


class LoginForm(Form):
    email = StringField(validators=[DataRequired(),
                                    Length(min=8, max=64),
                                    Email(message="电子邮箱不符合规定")])
    password = PasswordField(validators=[DataRequired(message="密码不为空, 请输入密码"),
                                         Length(min=6, max=32)])


class EmailForm(Form):
    email = StringField(validators=[DataRequired(),
                                    Length(min=8, max=64),
                                    Email(message="电子邮箱不符合规定")])


class ResetPasswordForm(Form):
    password1 = PasswordField(
        validators=[DataRequired(), Length(6, 32, message='长度介于6-32个字符之间'),
                    EqualTo('password2', message='两次输入需要一致')])
    password2 = PasswordField(validators=[DataRequired(), Length(6, 32)])
