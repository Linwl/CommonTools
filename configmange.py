#!usr/bin/env python
# coding=utf-8

"""
@company:广东浩迪创新科技有限公司
@version: ??
@author: linwl
@file: configmange.py
@time: 2017/7/28 15:16
@function：配置文件管理模块
"""
import configparser

class ConfigMange(object):

    def __init__(self,path):
        '''
        :param path: 文件所在的路径
        '''
        self.config = configparser.ConfigParser()
        self.config.read(path)

    def get_configstr(self,config_head,config_item):
        '''
        :param config_head:配置文件头
        :param config_item:配置文件项
        :return: 返回字符串配置项
        '''
        return self.config.get(config_head, config_item)

    def get_configint(self,config_head,config_item):
        '''
        :param config_head: 配置文件头
        :param config_item: 配置文件项
        :return: 返回int类型配置项
        '''
        return int(self.config.get(config_head, config_item))

    def get_exchangeconfig(self,configtitle):
        '''
        返回MQ交换机配置信息
        :param configtitle: 配置文件头名字
        :return:
        '''
        exchange = self.get_configstr(configtitle, 'exchange')
        exchange_type = self.get_configstr(configtitle, 'exchange_type')
        return exchange,exchange_type

    def get_queueconfig(self,configtitle):
        '''
        返回MQ队列配置信息
        :param configtitle: 配置文件头名字
        :return:
        '''
        queue_key = self.get_configstr(configtitle, 'rpc_key')
        queue_name = self.get_configstr(configtitle, 'queue')
        queue_consumertag = self.get_configstr(configtitle, 'consumer_tag')
        return queue_key,queue_name,queue_consumertag

    def get_dbconnconfig(self,configtitle):
        '''
        返回db数据库配置信息
        :param configtitle:
        :return:
        '''
        name = self.get_configstr(configtitle, 'name')
        passwd = self.get_configstr(configtitle, 'passwd')
        host = self.get_configstr(configtitle, 'host')
        port = self.get_configstr(configtitle, 'port')
        db_name = self.get_configstr(configtitle, 'db_name')
        return name,passwd,host,port,db_name

    def get_redisconfig(self,configtitle):
        '''
        返回redis连接配置信息
        :param configtitle:
        :return:
        '''
        host = self.get_configstr(configtitle, 'ip')
        port = self.get_configint(configtitle, 'port_one')
        db = self.get_configstr(configtitle, 'db')
        return host,port,db


    def get_mqconnconfig(self,configtitle):
        '''
        返回MQ连接配置信息
        :param configtitle:
        :return:
        '''
        username = self.get_configstr(configtitle, 'username')
        password = self.get_configstr(configtitle, 'password')
        ip = self.get_configstr(configtitle, 'ip')
        port = self.get_configint(configtitle, 'port')
        host = self.get_configstr(configtitle, 'vhost')
        return username,password,ip,port,host

    def items(self,node):
        '''
        获取节点内容
        :param node:
        :return:
        '''
        try:
            return self.config.items(node)
        except Exception as e:
            raise e

    def has_option(self,section,option):
        '''
        是否有该项值
        :param section:
        :return:
        '''
        try:
            return self.config.has_option(section,option)
        except Exception as e:
            raise e

    def get_mongoconfig(self, configtitle):
        '''
        返回mongo连接配置信息
        :param configtitle:
        :return:
        '''
        host = self.get_configstr(configtitle, 'ip')
        port = self.get_configint(configtitle, 'port_one')
        db = self.get_configstr(configtitle, 'db')
        account = self.get_configstr(configtitle, 'account')
        collection = self.get_configstr(configtitle, 'collection')
        password = self.get_configstr(configtitle, 'password')
        return host, port, db,collection,account,password