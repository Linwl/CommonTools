#!usr/bin/env python
# coding=utf-8

"""
@company:
@version: ??
@author: linwl
@file: descriptortool.py
@time: 2018/1/15 16:03
@function：描述符工具模块
"""

import types

class TypedProperty(object):
    '''
    类型属性描述符
    '''
    def __init__(self,name,attr_type):
        self._name = '_'+name
        self._type = attr_type

    def __get__(self, instance, owner):
        print('getting:{0}'.format(self._name))
        return getattr(instance,self._name)

    def __set__(self, instance, value):
        print('setting:{0}'.format(value))
        if not isinstance(value, self._type):
            raise TypeError("<{0}>属性类型错误".format(self._type))
        setattr(instance,self._name, value)

    def __delete__(self, instance):
        raise AttributeError('Can not delete attribute')

class CommonProperty(object):
    '''
    类属性通用描述符
    '''
    def __init__(self,propert_yname):
        self._name = '_'+propert_yname

    def __get__(self, instance, owner):
        print('getting:{0}'.format(self._name))
        return getattr(instance,self._name)

    def __set__(self, instance, value):
        print('setting:{0}'.format(value))
        setattr(instance,self._name, value)

    def __delete__(self, instance):
        # print 'delete:{0}'.format(self._name)
        # delattr(instance,self._name)
        raise AttributeError('Can not delete attribute')

class multimethod(object):
    '''
    利用函数注解实现方法重载描述符
    '''
    def __init__(self,func):
        self._methods ={}
        self.__name__ = func.__name__
        self._default = func

    def match(self,*types):
        def register(func):
            ndefaults = len(func.__defaults__) if func.__defaults__ else 0
            for n in range(ndefaults + 1):
                self._methods[types[:len(types) - n]] = func
            return self
        return register

    def __call__(self, *args, **kwargs):
        types = tuple(type(arg) for arg in args[1:])
        meth = self._methods.get(types, None)
        if meth:
            return meth(*args)
        else:
            return self._default(*args)

    def __get__(self, instance, owner):
        if instance is not None:
            return types.MethodType(self, instance)
        else:
            return self