#!/usr/bin/python
# -*- coding:utf-8 -*-


class TradeInfo:

    def __init__(self):
        self.total = 0
        self.trades = []

    def process_all(self, goods):
        self.total = len(goods)
        self.trades = [self.__process_single(good) for good in goods]

    @classmethod
    def __process_single(cls, single):
        if single.create_datetime:
            time = single.create_datetime.strftime('%Y-%m-%d')
        else:
            time = '未知'
        return {
            'user_name': single.user.nickname,
            'time': time,
            'id': single.id
        }
