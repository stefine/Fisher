from flask import render_template

from app.models.gift import Gift
from app.spider.yushu_book import Yushubook
from app.viewmodel.book import BookViewModel
from . import web


@web.route('/')
def index():
    recent = Gift.recent()
    yushu_book = Yushubook()
    for r in recent:
        yushu_book.search_by_isbn(r.isbn)
    result = BookViewModel.collection(data=yushu_book)
    return render_template('index.html', recent=result['books'])


@web.route('/personal')
def personal_center():
    pass
