#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Float, Boolean
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app import login_manager
from app.libs.enums import PendingStatus
from app.libs.helper import is_isbn_or_query
from app.models.base import Base, db
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import Yushubook
from fisher import app


class User(Base, UserMixin):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=True)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, unique=False, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    _password = Column(String(100))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self.password, raw)

    def can_save_to_list(self, isbn):
        if is_isbn_or_query(isbn) == 'isbn':
            yushu_book = Yushubook()
            yushu_book.search_by_isbn(isbn)
            if not yushu_book.books[0]:
                return False
            gift_query = Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
            wish_query = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
            if not gift_query and not wish_query:
                return True
            else:
                return False
        return False

    def get_id(self):
        return self.id

    def generate_token(self, expiration=600):
        serializer = Serializer(app.config['SECRET_KEY'], expiration)
        return serializer.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        serializer = Serializer(app.config['SECRET_KEY'])
        try:
            data = serializer.loads(token.encode('utf-8'))
        except:
            return False
        uid = data.get('id')
        with db.session.auto_commit():
            user = User.query.get(uid)
            user.password = new_password
        return True

    def can_send_drift(self):
        if self.beans < 1:
            return False
        success_gift_count = Gift.query.filter_by(launched=False, uid=self.id).count()
        success_receive_count = Drift.query.filter_by(requester_id=self.id,
                                                      pending=PendingStatus.success).count()
        if success_receive_count / 2 <= success_gift_count:
            return True
        else:
            return False

    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_receive=str(self.send_counter) + '/' + str(self.receive_counter)
        )


@login_manager.user_loader
def get_user(uid):
    return User.query.get(uid)
