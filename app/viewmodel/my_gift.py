#!/usr/bin/python
# -*- coding:utf-8 -*-

from app.spider.yushu_book import Yushubook
from app.viewmodel.book import BookViewModel


class GiftViewModel:

    def __init__(self, gifts, wish_count):
        self.__gifts = gifts
        self.__isbn_list = wish_count

    def assamble(self):
        count = 0
        r = []
        for gift in self.__gifts:
            for item in self.__isbn_list:
                if gift.isbn == item['isbn']:
                    count = item['count']
                    yushu_book = Yushubook()
                    yushu_book.search_by_isbn(isbn=item['isbn'])
                    book = BookViewModel.collection(
                        data=yushu_book, query=gift.isbn)['books'][0]
                    temp = {
                        'id': gift.id,
                        'book': book,
                        'wishes_count': count
                    }
                    r.append(temp)
        return r
