#!usr/bin/env python
# coding=utf-8

"""
@company:广东浩迪创新科技有限公司
@version: ??
@author: linwl
@file: httptools.py
@time: 2018/6/28 17:20
@function：Http工具类
"""

import requests
from desTools import DesTools
import datetime
import time

class HttpRequestTools(object):
    __access_token = 'epcloudtokenkey20150508'

    @staticmethod
    def http_get(url,params =None,headers =None,timeout=7,add_auth = True):
        """
        HTTP Get请求
        :param url: 请求url
        :param payload: 参数字典
        :param headers: 请求头
        :param timeout: 超时时间
        :param add_auth: 是否设置身份验证
        :return:
        """
        headers = HttpRequestTools.__addheaders(add_auth, headers)
        res = requests.get(url, params=params, headers=headers, timeout=timeout)
        return res.text

    @staticmethod
    def http_post(url,data,headers=None, timeout=7, add_auth=True):
        """
        HTTP Post请求犯法
        :param url: 请求url
        :param data: 请求数据
        :param headers: 请求头
        :param timeout: 超时
        :param add_auth: 是否设置身份验证
        :return:
        """
        headers = HttpRequestTools.__addheaders(add_auth, headers)
        res = requests.post(url,data=data, headers=headers, timeout=timeout)
        return res.text

    @staticmethod
    def __addheaders(add_auth,headers):
        if headers is None:
            headers = {
                'Content-Type': 'application/json'
            }
        if add_auth:
            authorization = HttpRequestTools.__create_authorization()
            headers.setdefault('Authorization', authorization)
        return headers

    @classmethod
    def __create_authorization(cls):
        '''
        创建请求头
        :return:
        '''
        i = datetime.datetime.now()
        time_struct = time.mktime(i.timetuple())
        utc_tran = datetime.datetime.utcfromtimestamp(time_struct)
        datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        utctime = utc_tran.strftime('%Y%m%d%H%M%S')
        authorizationText = 'HDACS access_token={0};request_time={1}'.format(cls.__access_token,utctime)
        res = DesTools.encrypt(authorizationText)
        return res