#!usr/bin/env python
# coding=utf-8

"""
@company:
@version: ??
@author: linwl
@file: performanceTools.py
@time: 2018/10/26 10:06
@function：
"""

from functools import wraps
from datetime import datetime

def cal_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        t1 = datetime.now()
        result = func(*args, **kwargs)
        t2 = datetime.now()
        print("{0} running time:{1}秒!".format(func.__name__, (t2 - t1)))
        return result
    return wrapper