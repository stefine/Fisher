# -*- coding: utf-8 -*-
__author__ = 'bliss'

from enum import Enum


class PendingStatus(Enum):
    """交易状态"""
    waiting = 1
    success = 2
    reject = 3
    redraw = 4

    @classmethod
    def pending_str(cls, status, key):
        key_map ={
            cls.waiting:{
                'requester': '等待对方邮寄',
                'gifter': '等待你邮寄'
            },
            cls.success:{
                'requester': '对方已经邮寄',
                'gifter': '你已经邮寄'
            },
            cls.reject:{
                'requester': '对方已经拒绝',
                'gifter': '你已经拒绝'
            },
            cls.redraw:{
                'requester': '对方已经撤回',
                'gifter': '你已经撤回'
            }
        }
        return key_map[status][key]

