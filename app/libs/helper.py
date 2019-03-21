#!/usr/bin/python
# -*- coding:utf-8 -*-


def is_isbn_or_query(q):
    is_isbn_or_key = "query"
    if len(q) == 13 and q.isdigit():
        is_isbn_or_key = "isbn"
    q = q.replace("-", "")
    if q.isdigit() and len(q) == 10:
        is_isbn_or_key = "isbn"
    return is_isbn_or_key


