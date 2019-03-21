#!/usr/bin/python
# -*- coding:utf-8 -*-


class BookViewModel:

    @classmethod
    def collection(cls, query=None, data=None):
        returned = {
            'books': [],
            'total': 0,
            'keyword': query
        }
        if data:
            books = [cls.__cut_data(b) for b in data.books]
            total = data.total
            returned = {
                'books': books,
                'total': total,
                'keyword': query
            }
        return returned

    @classmethod
    def __cut_data(cls, data):
        book = {
            'title': data['title'],
            'publisher': data['publisher'],
            'pages': data['pages'] or '',
            'author': ', '.join(data['author']),
            'price': data['price'],
            'image': data['image'],
            'summary': data['summary'] or '',
            'isbn': data['isbn'],
            'pubdate': data['pubdate'],
            'binding': data['binding']
        }
        intro = filter(lambda x: True if x else False,
                       [book['author'], book['publisher'], book['price']])
        intro = '/'.join(intro)
        book['intro'] = intro
        return book





