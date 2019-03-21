#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask_login import current_user

from app.forms.book import SearchForm
from app.models.gift import Gift
from app.models.wish import Wish
from app.viewmodel.trade_info import TradeInfo
from app.web import web
from app.libs.helper import is_isbn_or_query
from app.spider.yushu_book import Yushubook
from flask import request, render_template, url_for, redirect, flash

from app.viewmodel.book import BookViewModel


@web.route("/book/search", methods=['GET'])
def search():
    form = SearchForm(request.args)
    result = BookViewModel.collection()
    if form.validate():
        page = form.page.data
        query = form.q.data.strip()
        res = is_isbn_or_query(query)
        yushu_book = Yushubook()
        if res == "isbn":
            yushu_book.search_by_isbn(query)
        else:
            yushu_book.search_by_query(query, page)
        result = BookViewModel.collection(data=yushu_book, query=query)
        return render_template("search_result.html", books=result)
    flash("搜索关键字不符合要求，请重新输入")
    return render_template("search_result.html", books=result)


@web.route("/book/<isbn>/detail")
def book_detail(isbn):
    has_in_wishes = False
    has_in_gifts = False

    yushu_book = Yushubook()
    yushu_book.search_by_isbn(isbn)
    result = BookViewModel.collection(data=yushu_book, query=isbn)

    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id,
                                isbn=isbn, launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id,
                                isbn=isbn, launched=False).first():
            has_in_wishes = True

    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

    # print(trade_gifts)

    trade_gifts_model = TradeInfo()
    trade_gifts_model.process_all(trade_gifts)
    trade_wishes_model = TradeInfo()
    trade_wishes_model.process_all(trade_wishes)

    return render_template("book_detail.html", book=result['books'][0],
                           has_in_wishes=has_in_wishes, has_in_gifts=has_in_gifts,
                           wishes=trade_wishes_model, gifts=trade_gifts_model)


# 通过 endpoint 能使得 url_for 找到 view_function hello()
@web.route("/hello/", endpoint="hi")
def hello():
    flash("xuxu is watching TV")
    return render_template("test.html")


@web.route("/test/")
def test():
    return redirect(url_for(endpoint="web.hi"))
