#!usr/bin/env python
# coding=utf-8

"""
@company:
@version: ??
@author: linwl
@file: mongodbmanage.py
@time: 2018/7/31 9:07
@function：mongodb管理模块
"""
import threading
from configmange import ConfigMange
from pymongo import MongoClient

class MongodbManage:
    # 模块版本号
    _Version = "1.0.02"

    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                cls._instance = object.__new__(cls)
                cls._instance.initialize(*args, **kwargs)
        return cls._instance

    def __init__(self,*args,**kwargs):
        pass

    def __str__(self):
        return '(MongodbManage:Mongodb管理模块)'

    def initialize(self, *args, **kwargs):
        """
        只初始化一次配置
        :param args:
        :param kwargs:
        :return:
        """
        try:
            path = kwargs.get('path')
            config = ConfigMange(path)
            host, port, db_name, collection_name,self.account,self.password= config.get_mongoconfig('MongoDb')
            self._conn = MongoClient(host, port)
            self._db = getattr(self._conn,db_name)
            self._db.authenticate(self.account, self.password)
            self._collection =getattr(self._db,collection_name)
        except Exception as e:
            error_msg = '连接Mongo配置出现异常:{0}!'.format(e)
            raise RuntimeError(error_msg)


    def query_all(self,db=None,collection=None):
        '''
        获取指定MongoDb数据库的集合所有数据
        :param db: 数据库
        :param collection: 集合
        :return:
        '''
        try:
            self._init_db(collection, db)
            return self._collection.find()
        except Exception as e:
            raise RuntimeError(e)

    def query_one(self,db=None,collection=None):
        '''
        获取指定MongoDb数据库的集合第一条数据
        :param db: 数据库
        :param collection: 集合
        :return:
        '''
        try:
            result = []
            append = result.append
            self._init_db(collection, db)
            cursor = self._collection.find_one()
            for c in cursor:
                append(c)
            return result
        except Exception as e:
            raise RuntimeError(e)

    def _init_db(self, collection, db):
        '''
        初始化mongodb数据库信息
        :param collection:
        :param db:
        :return:
        '''
        if db:
            self._db = getattr(self._conn, db)
            self._db.authenticate(self.account, self.password)
            if collection:
                self._collection = getattr(self._db, collection)
            else:
                raise ValueError('集合名不能为空!')
        else:
            pass

    def query_by_field(self,field_list,is_return = 1,collection =None,db =None):
        '''
        根指定字段查询数据
        :param field: 字段列表
        :param is_return: 0不返回指定字段值 1返回指定字段值
        :param collection: 操作集合
        :param db: 操作数据库
        :return:返回结果列表
        '''
        try:
            result =[]
            append = result.append
            if isinstance(field_list,list):
                if len(field_list) >0:
                    self._init_db(collection, db)
                    fields = {
                        k:is_return for k in field_list
                    }
                    cursor = self._collection.find({},fields)
                    for c in cursor:
                        append(c)
                else:
                    raise ValueError('字段列表参数不能为空!')
            else:
                raise TypeError('字段列表类型错误,非list类型')
            return result
        except Exception as e:
            raise RuntimeError(e)

    def find(self,query,collection =None,db =None):
        '''
        根据指定条件查询
        :param query:
        :param collection:
        :param db:
        :return:返回结果列表
        '''
        try:
            result =[]
            append = result.append
            self._init_db(collection, db)
            if query:
                cursor = self._collection.find(query)
                for c in cursor:
                    append(c)
            else:
                raise ValueError('查询参数不能为空!')
            return result
        except Exception as e:
            raise RuntimeError(e)

    def insert_one(self,params,collection =None,db =None):
        """
        单条插入
        :param params: 插入参数字典
        :param collection: 操作指定集合
        :param db: 操作指定数据库
        :return:
        """
        try:
            if isinstance(params,dict):
                self._init_db(collection, db)
                return self._collection.insert_one(params).inserted_id
            else:
                raise TypeError('插入参数类型错误,非dict类型')
        except Exception as e:
            raise RuntimeError(e)

    def insert_many(self,params,collection =None,db =None):
        """
        插入多条记录
        :param params:
        :param collection:
        :param db:
        :return:
        """
        try:
            if isinstance(params, list):
                self._init_db(collection, db)
                return self._collection.insert_many(params).inserted_ids
            else:
                raise TypeError('字段列表类型错误,非list类型')
        except Exception as e:
            raise RuntimeError(e)

    def delete_one(self,params,collection =None,db =None):
        """
        单条删除
        :param params: 删除参数字典
        :param collection: 操作指定集合
        :param db: 操作指定数据库
        :return:
        """
        try:
            if isinstance(params,dict):
                self._init_db(collection, db)
                self._collection.delete_one(params)
            else:
                raise TypeError('删除参数类型错误,非dict类型')
        except Exception as e:
            raise RuntimeError(e)

    def delete_many(self,params,collection =None,db =None):
        """
        多条删除
        :param params: 删除参数字典
        :param collection: 操作指定集合
        :param db: 操作指定数据库
        :return:删除的个数
        """
        try:
            if isinstance(params,dict):
                self._init_db(collection, db)
                return self._collection.delete_many(params).deleted_count
            else:
                raise TypeError('删除参数类型错误,非dict类型')
        except Exception as e:
            raise RuntimeError(e)

    def update_one(self,query_params,newvalues,collection =None,db =None):
        '''
        更新单条记录
        :param query_params:
        :param newvalues:
        :param collection:
        :param db:
        :return:
        '''
        try:
            if isinstance(query_params, dict) and isinstance(newvalues, dict):
                self._init_db(collection, db)
                self._collection.update_one(query_params,{"$set": newvalues})
            else:
                raise TypeError('插入参数类型错误,非dict类型')
        except Exception as e:
            raise RuntimeError(e)

    def update_many(self,query_params,newvalues,collection =None,db =None):
        """
        同时更新多条记录
        :param query_params:
        :param newvalues:
        :param collection:
        :param db:
        :return:返回更新记录条数
        """
        try:
            if isinstance(query_params, dict) and isinstance(newvalues, dict):
                self._init_db(collection, db)
                return self._collection.update_many(query_params, {"$set": newvalues}).modified_count
            else:
                raise TypeError('插入参数类型错误,非dict类型')
        except Exception as e:
            raise RuntimeError(e)