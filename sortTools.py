#!usr/bin/env python
# coding=utf-8

"""
@company:广东浩迪创新科技有限公司
@version: ??
@author: linwl
@file: sortTools.py
@time: 2018/10/24 16:14
@function：
"""


class SortTools:

    @classmethod
    def quick_sort(cls,array):
        """
        快速排序算法
        :param array: 排序数组
        :return:
        """
        if len(array) < 2:  # 基线条件（停止递归的条件）
            return array
        else:  # 递归条件
            baseValue = array[0]  # 选择基准值
            # 由所有小于基准值的元素组成的子数组
            less = [m for m in array[1:] if m < baseValue]
            # 包括基准在内的同时和基准相等的元素
            equal = [w for w in array if w == baseValue]
            # 由所有大于基准值的元素组成的子数组
            greater = [n for n in array[1:] if n > baseValue]
        return cls.quick_sort(less) + equal + cls.quick_sort(greater)

if __name__ == '__main__':
    myList = [49, 38, 65, 97, 76, 13, 27, 49]
    print("Quick Sort: ")
    print(SortTools.quick_sort(myList))
