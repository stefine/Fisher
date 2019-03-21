#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests


class HTTP:
    @staticmethod
    def get(url, return_json=True):
        r = requests.get(url)
        if r.status_code == 200:
            if return_json:
                return r.json()
        else:
            return r.next
        return {} if r.status_code != 200 and return_json else ""

