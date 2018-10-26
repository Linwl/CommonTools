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
        middle = (low +high)// 2
        if arry[middle] == item:
            return '待查元素{0}在列表中下标为：{1}'.format(item, middle)
        elif arry[middle] > item:
            high = middle - 1
        else:
            low = middle + 1
    return '待查找元素%s不存在指定列表中'%item

@cal_time
def interpolation__search(arry,item):
    """
    插值查找算法
    :param arry: 源数组
    :param item: 目标
    :return:
    """
    low = 0
    high = len(arry) -1
    arry = SortTools.quick_sort(arry)
    time = 0
    while low < high:
        time += 1
        # 计算mid值是插值算法的核心代码
        mid = low + int((high - low) * (item - arry[low]) / (arry[high] - arry[low]))
        if arry[mid] == item:
            # 打印查找的次数
            print("times: %s" % time)
            return '待查元素{0}在列表中下标为：{1}'.format(item, mid)
        elif item < arry[mid]:
            high = mid - 1
        else:
            low = mid + 1
    return '待查找元素%s不存在指定列表中'%item

if __name__ == '__main__':
    arry = [4,5,9,3,1,7]
    print(binary_search(arry,4))
    print(interpolation__search(arry, 4))