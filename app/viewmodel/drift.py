#!/usr/bin/python
# -*- coding:utf-8 -*-

from app.libs.enums import PendingStatus


class DriftViewModel:

    def __init__(self, drifts, current_user_id):
        self.drifts = drifts
        self.current_user_id = current_user_id

    def collection(self):
        return [self.__parse(drift) for drift in self.drifts]

    def requester_or_gifter(self, drift):
        if self.current_user_id == drift.gifter_id:
            you_are = 'gifter'
        else:
            you_are = 'requester'
        return you_are

    def __parse(self, drift):
        you_are = self.requester_or_gifter(drift)
        pending_status = PendingStatus.pending_str(drift.pending, you_are)
        r = {
            'drift_id': drift.id,
            'you_are': you_are,
            'book_title': drift.book_title,
            'book_author': drift.book_author,
            'book_img': drift.book_img,
            'operator': drift.requester_nickname if you_are != 'requester' else drift.gifter_nickname,
            'date': drift.create_datetime.strftime('%Y-%m-%d'),
            'message': drift.message,
            'address': drift.address,
            'recipient_name': drift.recipient_name,
            'mobile': drift.mobile,
            'status_str': pending_status,
            'status': drift.pending
        }
        return r
