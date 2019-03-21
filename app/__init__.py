#!/usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail


login_manager = LoginManager()
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.settings")
    app.config.from_object("app.secure")
    register_blue(app)
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录注册'

    from app.models.base import db
    db.init_app(app)
    # db.drop_all(app=app)
    db.create_all(app=app)
    return app


def register_blue(app):
    from app.web.book import web
    app.register_blueprint(web)


