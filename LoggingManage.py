#!usr/bin/env python
# coding=utf-8

"""
@company:广东浩迪创新科技有限公司
@version: ??
@author: linwl
@file: LoggingManage.py
@time: 2017/7/28 15:16
@function：日志文件管理模块
"""

import logging.config
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import re
import platform
from metaclasstool import Cached

class LogginMange(object):
    """
    Logging模块管理
    """
    _Version='1.0.2018.01.15'
    #通过配置文件路径设置日志参数

    __metaclass__ = Cached

    def __init__(self,logname,Logger):
        try:
            sysstr = platform.system()
            if (sysstr == "Windows"):
                work_path = os.getcwd() + '\Log'
                logg_path = r'Log\%s' % logname
            elif (sysstr == "Linux"):
                work_path = os.getcwd() + '/Log'
                logg_path = r'Log/%s' % logname
            else:
                print("Other System")

            if not os.path.exists(work_path):
                os.makedirs(work_path)
            else:
                print(u'Log文件夹已存在')
            # 创建一个logger
            logger = logging.getLogger(Logger)
            logger.setLevel(logging.DEBUG)
            # 创建一个handler，用于写入日志文件

            LOG_FILE =logg_path +'.log'
            self.fh = TimedRotatingFileHandler(filename=LOG_FILE, when ='MIDNIGHT', interval=1,backupCount=30)
            self.fh.suffix = "%Y-%m-%d.log"
            self.fh.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
            self.fh.setLevel(logging.DEBUG)
            # 再创建一个handler，用于输出到控制台
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            # 定义handler的输出格式
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            self.fh.setFormatter(formatter)
            ch.setFormatter(formatter)
            # 给logger添加handler
            logger.addHandler(self.fh)
            logger.addHandler(ch)
            self.logger = logger
        except Exception as e:
            raise e

    def remove_handler(self):
        self.logger.removeHandler(self.fh)

    def debug(self,msg):
        self.logger.debug(msg)

    def info(self,msg):
        self.logger.info(msg)

    def warning(self,msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def __str__(self):
        return '(LogginMange:日志管理模块)'