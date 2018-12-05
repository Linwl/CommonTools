#!usr/bin/env python
# coding=utf-8

"""
@company:
@version: ??
@author: linwl
@file: metaclasstool.py
@time: 2018/1/15 9:26
@function：元类模块
"""
import weakref
import threading

class Singleton(type):
    '''
    单例元类
    '''
    _instance_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with Singleton._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance

class Cached(type):
    '''
    缓存元类
    '''

    def __init__(self,*args,**kwargs):
        super(Cached,self).__init__(*args,**kwargs)
        self.__cache = weakref.WeakValueDictionary()

    def __call__(self, *args, **kwargs):
        if args in self.__cache:
            return self.__cache[args]
        else:
            obj = super(Cached,self).__call__(*args, **kwargs)
            self.__cache[args] = obj
            return obj