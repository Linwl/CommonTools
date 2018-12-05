#!usr/bin/env python
# coding=utf-8

"""
@company:
@version: ??
@author: linwl
@file: jsontools.py
@time: 2017/7/28 14:39
@function：Json工具类
"""
import datetime
import json
import uuid
from decimal import Decimal


class JsonHelper(object):

    @staticmethod
    def encode(obj,ensure_ascii=True):
        '''
        把传进来的对象格式化成json格式
        :param obj:
        :return:
        '''
        try:
            jsontext = json.dumps(obj,ensure_ascii=ensure_ascii,default=JsonHelper.default)
            return jsontext
        except UnicodeEncodeError as e:
            raise e
        except TypeError as e:
            raise e
        except Exception as e:
            raise e

    @classmethod
    def decode(cls,jsontext,encoding=None):
        '''
        把传进来的字符串格式化成python对象
        :param jsontext:
        :return:
        '''
        try:
            return cls._byteify(
                json.loads(jsontext,encoding=encoding, object_hook=cls._byteify),
                ignore_dicts=True
            )
        except UnicodeEncodeError as e:
            raise e
        except TypeError as e:
            raise e
        except Exception as e:
            raise e

    @staticmethod
    def encode_obj(obj):
        '''
        把传进来的python对象格式化成json格式
        :param obj:
        :return:
        '''
        try:
            obj = obj.__dict__
            jsontext = json.dumps(obj, ensure_ascii=False,default=JsonHelper.default)
            return jsontext
        except UnicodeEncodeError as e:
            raise e
        except TypeError as e:
            raise e
        except Exception as e:
            raise e

    @staticmethod
    def default(obj):
        '''
        python类型自定义处理
        :param obj:
        :return:
        '''
        if isinstance(obj, Decimal):
            return str(obj)
        elif isinstance(obj,datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj,datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj,uuid.UUID):
            return str(obj)

    @staticmethod
    def _byteify(data, ignore_dicts = False):
        # if this is a list of values, return list of byteified values
        if isinstance(data, list):
            return [JsonHelper._byteify(item, ignore_dicts=True) for item in data]
        # if this is a dictionary, return dictionary of byteified keys and values
        # but only if we haven't already byteified it
        if isinstance(data, dict) and not ignore_dicts:
            return {
                JsonHelper._byteify(key, ignore_dicts=True): JsonHelper._byteify(value, ignore_dicts=True)
                for key, value in data.items()
            }
        return data
