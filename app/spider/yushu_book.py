#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import jsonify, current_app

from app.libs.HTTP import HTTP


class Yushubook:
    isbn_url = "http://t.yushu.im/v2/book/isbn/{}"
    q_url = "http://t.yushu.im/v2/book/search?q={}&count={}&start={}"

    def __init__(self):
        self.books = []
        self.total = 0

    def search_by_isbn(self, isbn):
        url = Yushubook.isbn_url.format(isbn)
        self.__single(HTTP.get(url))

    def search_by_query(self, query, page):
        per = current_app.config["PERPAGE"]
        url = Yushubook.q_url.format(query, per, (page-1)*per)
        self.__collection(HTTP.get(url))

    def __single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    def __collection(self, data):
        self.total = data['total']
        self.books = data['books']

