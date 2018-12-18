#!usr/bin/env python
# coding=utf-8

"""
@company:
@version: ??
@author: linwl
@file: multiprocessTools.py
@time: 2018/12/5 9:14
@function：多进程工具类
"""
import os
from queue import Empty
from multiprocessing import Process,Manager,Event
import time

class ProcessPool:
    """
    多进程池类
    """
    WORKERS = 1 #工作者数量

    def __init__(self,processes=None,isStart =True,sleepTime=0.1):
        """
        多进程池初始化函数
        :param processes: 进程个数
        :param isStart: 是否立即启动
        :param sleepTime:进程休眠时间
        """
        if processes is None:
            processes = os.cpu_count() or 1
        if processes < 1:
            raise ValueError("Number of processes must be at least 1")

        self.WORKERS = processes
        self.workers = []  # 工作者列表
        self.dismissedWorkers = []  # 休眠工作者列表
        self._manager = Manager()
        self._resultQueue = self._manager.Queue()
        self._workQueue = self._manager.Queue()
        self._createWorkers(sleepTime)
        self._workers_start(isStart)

    def _workers_start(self,isStart):
        """
        工作者进程启动
        :param isStart:
        :return:
        """
        try:
            if isStart:
                for worker in self.workers:
                    if not worker.is_alive():
                        worker.start()
        except Exception as e:
            raise e

    def _createWorkers(self,sleepTime):
        """
        创建工作者进程
        :param sleepTime:休眠时间
        :return:
        """
        append =self.workers.append
        for i in range(self.WORKERS):
            worker = WorkProcess(resultQueue=self._resultQueue,taskQueue=self._workQueue,timeout=sleepTime)
            worker.daemon =True
            append(worker)

    def start(self):
        """
        进程池启动
        :return:
        """
        self._workers_start(True)

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

    def get_result(self, block=True, timeout=None):
        '''
        获取任务结果
        :param block:
        :param timeout:
        :return:
        '''
        try:
            item = self._resultQueue.get(block, timeout)
            return item
        except Empty as e:
            return None
        except Exception as e:
            raise e

    def get_nowait(self):
        """
        不阻塞获取任务结果
        :return:
        """
        try:
            item = self._resultQueue.get_nowait()
            return item
        except Empty as e:
            raise e
        except Exception as e:
            raise e

    def close(self):
        """
        进程池关闭
        :return:
        """
        try:
            self._dismissWorkers(self.WORKERS)
        except Exception as e:
            raise e

    def wait_for_complete(self,timeout=0.1):
        """
        阻塞并获取线程池结果
        :param timeout:阻塞时间
        """
        while True:
            workerNums = self._workQueue.qsize()#获取任务队列数量
            runWorkers = len(self.workers)
            if workerNums == 0:
                time.sleep(timeout)
                self._dismissWorkers(runWorkers)
                break
            time.sleep(timeout)
        self._joinAllDissmissedWorkers()

    def _joinAllDissmissedWorkers(self):
        """
        挂起所有闲置工作线程者
        """
        for worker in self.dismissedWorkers:
            worker.join()
        self.dismissedWorkers = []


    def _dismissWorkers(self, workerNums, _join=False):
        '''
        通知进程休眠
        :param workerNums: 工作进程数量
        :param _join:是否挂起
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


class WorkProcess(Process):
    """
    工作者进程
    """
    EXITCODE = None
    ERRORMSG = None

    def __init__(self,taskQueue,resultQueue,timeout=0.1,**kwargs):
        super(WorkProcess,self).__init__(**kwargs)
        self._taskQueue = taskQueue
        self._resultQueue = resultQueue
        self._dismissed = Event()
        self._timeout =timeout

    def run(self):
        """
        进程工作函数
        :return:
        """
        while 1:
            if self._dismissed.is_set():
                break
            self.EXITCODE = 0
            self.ERRORMSG = None
            try:
                callable,args, kwargs = self._taskQueue.get(block=True,timeout=self._timeout)
            except Empty:
                continue
            except Exception as e:
                self.EXITCODE = 1001
                self.ERRORMSG = "Process<{0}> get the task error:{1}!".format(os.getpid(),e)
                self._resultQueue.put((self.EXITCODE,(callable, args, kwargs), self.ERRORMSG))
                break

            if self._dismissed.is_set():
                self._taskQueue.put((callable, args, kwargs))
                break

            try:
                result = callable(*args, **kwargs)
                self._resultQueue.put((self.EXITCODE, result, self.ERRORMSG))
            except Exception as e:
                self.EXITCODE = 1002
                self.ERRORMSG = "Process<{0}> perform tasks error:{1}!".format(os.getpid(), e)
                self._resultQueue.put((self.EXITCODE,(callable, args, kwargs), self.ERRORMSG))

    def dismiss(self):
        """
        发送进程终止信息
        :return:
        """
        self._dismissed.set()