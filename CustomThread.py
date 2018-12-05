#!usr/bin/env python
# coding=utf-8

"""
@company:
@version: ??
@author: linwl
@file: CustomThread.py
@time: 2017/7/29 9:28
@function：线程模块
"""
import threading
import datetime
import sys,traceback
import StringIO
import Queue
import time

class CustomThread(threading.Thread):
    def __init__(self,log, func, args='', name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args
        self.log = log
        self.exitcode = 0 #异常码
        self.exception = None
        self.exc_traceback = ''

    def getresult(self):
        return self.result

    def _run(self):
        start_msg = u'线程[%s]在%s启动 ' % (self.name, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.log.info(start_msg)
        if isinstance(self.args, list):
            self.result = self.func(*self.args)
        elif isinstance(self.args, dict):
            self.result = self.func(**self.args)
        else:
            self.result = self.func()
        end_msg = u'线程[%s]在%s结束 ' % (self.name, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.log.info(end_msg)

    def run(self):
        try:
            self._run()
        except Exception as e:
            self.exitcode = 1  # 如果线程异常退出，将该标志位设置为1，正常退出为0
            self.exception = e
            self.exc_traceback = ''.join(traceback.format_exception(*sys.exc_info()))  # 在改成员变量中记录异常信息

class ExcThread(threading.Thread):
    '''
    返回线程异常模块
    '''

    def __init__(self,log,func,bucket,args='', name='',):
        threading.Thread.__init__(self)
        self.name = name
        self.log = log
        self.func = func
        self.args = args
        self.bucket = bucket

    def getresult(self):
        return self.result

    def _run(self):
        start_msg = '线程[%s]在%s启动 ' % (self.name, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.log.info(start_msg)
        if isinstance(self.args, list):
            self.result = self.func(*self.args)
        elif isinstance(self.args, dict):
            self.result = self.func(**self.args)
        else:
            self.result = self.func()
        end_msg = '线程[%s]在%s结束 ' % (self.name, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.log.info(end_msg)

    def run(self):
        try:
            self._run()
        except Exception as e:
            exc_info =''.join(traceback.format_exception(*sys.exc_info()))
            exstr =  '子线程<{0}>发生异常:{1}'.format(self.name,exc_info)
            self.bucket.put(exstr)

class WorkThread(threading.Thread):
    '''
    工作线程者类
    '''
    def __init__(self, workQueue, resultQueue, timeout=0.1, **kwargs):
        threading.Thread.__init__(self, **kwargs)
        self.setDaemon(True)
        self._workQueue = workQueue
        self._resultQueue = resultQueue
        self._timeout = timeout
        self._dismissed = threading.Event()
        self.start()

    def run(self):
        '''
        重复处理任务直到被告知退出
        :return:
        '''
        while 1:
            if self._dismissed.isSet():
                break

            handlerKey = None  # unique key
            code = 0  # callback return code
            result = None
            errMsg = ""

            try:
                callable, args, kwargs = self._workQueue.get(True, self._timeout)
            except Queue.Empty:
                continue
            except:
                exceptMsg = StringIO.StringIO()
                traceback.print_exc(file=exceptMsg)
                errMsg = exceptMsg.getvalue()
                code = 3301  # system error
                self._resultQueue.put(
                        (handlerKey, code, (callable, args, kwargs), errMsg))
                break

            if self._dismissed.isSet():
                self._workQueue.put((callable, args, kwargs))
                break

            try:
                if "handlerKey" in kwargs:
                    handlerKey = kwargs["handlerKey"]
                result = callable(*args, **kwargs)  # block
                self._resultQueue.put((handlerKey, code, result, errMsg))
            except:
                exceptMsg = StringIO.StringIO()
                traceback.print_exc(file=exceptMsg)
                errMsg = exceptMsg.getvalue()
                code = 3303
                self._resultQueue.put((handlerKey, code, result, errMsg))

    def dismiss(self):
        """
        发送线程终止信息
        :return:
        """
        self._dismissed.set()

class ThreadPool(object):
    '''
    线程池模块
    '''
    _Version = "1.0.2018.07.18"
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                cls._instance = object.__new__(cls, *args, **kwargs)
                cls._instance.initialize(*args, **kwargs)
        return cls._instance

    def initialize(self,workerNums=3, timeout=0.1,resultQueue =None):
        '''
        线程池初始化函数
        :param workerNums: 工作者个数
        :param timeout: 超时时间
        :return:
        '''
        self._workerNums = workerNums
        self._timeout = timeout
        self._workQueue = Queue.Queue()
        if resultQueue:
            self._resultQueue = resultQueue
        else:
            self._resultQueue = Queue.Queue()
        self.workers = [] #工作者列表
        self.dismissedWorkers = [] #休眠工作者列表
        self._createWorkers(self._workerNums)

    def __init__(self,workerNums=3, timeout=0.1,resultQueue =None):
        '''
        默认线程池最大为3
        :param workerNums:
        :param timeout:
        :param resultQueue:
        '''
        pass

    def _createWorkers(self, workerNums):
        """
        创建工作者线程
        :param workerNums:
        :return:
        """
        append =self.workers.append
        for i in range(workerNums):
            worker = WorkThread(self._workQueue, self._resultQueue,
                              timeout=self._timeout)
            append(worker)


    def _dismissWorkers(self, workerNums, _join=False):
        '''

        :param workerNums: 工作线程数量
        :param _join:
        :return:
        '''
        dismissList = []
        for i in range(min(workerNums, len(self.workers))):
            worker = self.workers.pop()
            worker.dismiss()
            dismissList.append(worker)

        if _join:
            for worker in dismissList:
                worker.join()
        else:
            self.dismissedWorkers.extend(dismissList)

    def _joinAllDissmissedWorkers(self):
        """
        挂起所有闲置工作线程者
        """
        for worker in self.dismissedWorkers:
            worker.join()
        self.dismissedWorkers = []

    def add_task(self, callable, *args, **kwargs):
        '''
        添加任务
        :param callable:执行任务func
        :param args:
        :param kwargs:
        :return:
        '''
        if not self._workQueue.full():
            self._workQueue.put((callable, args, kwargs))
        else:
            raise StopIteration('Task Queue Is Full!')

    def getResult(self, block=False, timeout=0.1):
        '''
        获取任务结果
        :param block:
        :param timeout:
        :return:
        '''
        try:
            item = self._resultQueue.get(block, timeout)
            return item
        except Queue.Empty as e:
            return None
        except:
            raise

    def waitForComplete(self, timeout=0.1):
        """
        阻塞并获取线程池结果
        :param timeout:阻塞时间
        """
        while True:
            workerNums = self._workQueue.qsize()  # 释放掉所有线程
            runWorkers = len(self.workers)

            if 0 == workerNums:
                time.sleep(timeout)  # waiting for thread to do job
                self._dismissWorkers(runWorkers)
                break
            time.sleep(timeout)
        self._joinAllDissmissedWorkers()