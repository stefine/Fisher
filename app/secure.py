#!/usr/bin/python
# -*- coding:utf-8 -*-

DEBUG = True
SQLALCHEMY_DATABASE_URI = "mysql+cymysql://root:root@localhost:3306/fisher"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "\x88D\xf09"

# Email 配置
MAIL_SERVER = 'smtp.exmail.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TSL = False
MAIL_USERNAME = 'hello@qq.com'
MAIL_PASSWORD = 'xxxx'