#!usr/bin/env python
# coding=utf-8

"""
@company:广东浩迪创新科技有限公司
@version: ??
@author: linwl
@file: searchTools.py
@time: 2018/10/26 9:58
@function：查找算法工具
"""
from performanceTools import cal_time
from sortTools import SortTools

@cal_time
def binary_search(arry,item):
    """
    二分查找法
    :param arry: 源数组
    :param item: 目标
    :return:
    """
    low = 0
    high = len(arry) -1
    arry = SortTools.quick_sort(arry)
    while low < high:
        middle = int((low +high)/2)
        if arry[middle] == item:
            return '待查元素{0}在列表中下标为：{1}'.format(item, middle)
        elif arry[middle] > item:
            high = middle - 1
        else:
            low = middle + 1
    return '待查找元素%s不存在指定列表中'%item

if __name__ == '__main__':
    arry = [4,5,9,3,1,7]
    print(binary_search(arry,15))