#!/usr/bin/python
# -*- coding:utf-8 -*-

from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, desc, func
from sqlalchemy.orm import relationship
from app.models.base import Base, db


class Wish(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey("user.id"))
    isbn = Column(String(13))
    launched = Column(Boolean, default=False)

    @classmethod
    def get_user_wish(cls, uid):
        return Wish.query.filter_by(uid=uid, launched=False).order_by(
            desc(Wish.create_time)).all()

    @classmethod
    def wish_count(cls, isbn_list):
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).\
            filter(Wish.isbn.in_(isbn_list), Wish.status == 1, Wish.launched == False).\
            group_by(Wish.isbn).all()
        return [{'count': c[0], 'isbn':c[1]} for c in count_list]


