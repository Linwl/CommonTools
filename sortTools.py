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
import math
from collections import deque
from heapq import merge

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

    @staticmethod
    def selection_sort(array):
        """
        选择排序
        :param array:
        :return:
        """
        for i in range(0, len(array) - 1):
            min_ = i
            for j in range(i + 1, len(array)):
                if array[j] < array[min_]:
                    min_ = j
            array[i], array[min_] = array[min_], array[i]  # swap

    @classmethod
    def heap_sort(cls,array):
        """
        堆排序
        :param array: 排序数组
        :return:
        """
        L = deque(array)
        L.appendleft(0)
        L_length = len(L) - 1
        first_sort_count = int(L_length / 2)
        for i in range(first_sort_count):
            cls.make_heap(L,first_sort_count-i,L_length)

        for i in range(L_length - 1):
            L = cls.swap_param(L, 1, L_length - i)
            cls.make_heap(L, 1, L_length - i - 1)
        return [L[i] for i in range(1,len(L))]

    @classmethod
    def swap_param(cls,heap_L, i, j):
        """
        交换堆顶元素和最后元素
        :param heap_L: 大根堆序列
        :param i:
        :param j:
        :return:
        """
        heap_L[i], heap_L[j] = heap_L[j], heap_L[i]
        return heap_L

    @classmethod
    def make_heap(cls,heap_L,start,end):
        """
        创建大根堆序列
        :param heap_L:
        :param start:起始位置
        :param end:
        :return:
        """
        temp = heap_L[start]
        i = start
        j =i * 2
        while j <= end:
            if (j < end) and (heap_L[j] < heap_L[j + 1]):
                j += 1
            if temp < heap_L[j]:
                heap_L[i] = heap_L[j]
                i = j
                j = 2 * i
            else:
                break
        heap_L[i] = temp

    @staticmethod
    def insertion_sort(array):
        """
        直接插入排序
        :param array:
        :return:
        """
        lenth = len(array)
        for i in range(1,lenth):
            temp = array[i]
            j= i-1
            # temp与前一个元素比较，若temp较小则前一元素后移，j自减，继续比较
            while j >= 0 and temp < array[j]:
                array[j + 1] = array[j]
                j = j - 1
            # temp所指向元素的J向前一位位置
            array[j + 1] = temp

    @staticmethod
    def print_tree(array):
        '''
        深度 前空格 元素间空格
        1     7       0
        2     3       7
        3     1       3
        4     0       1
        '''
        # first=[0]
        # first.extend(array)
        # array=first
        index = 1
        depth = math.ceil(math.log2(len(array)))  # 因为补0了，不然应该是math.ceil(math.log2(len(array)+1))
        sep = '  '
        for i in range(depth):
            offset = 2 ** i
            print(sep * (2 ** (depth - i - 1) - 1), end='')
            line = array[index:index + offset]
            for j, x in enumerate(line):
                print("{:>{}}".format(x, len(sep)), end='')
                interval = 0 if i == 0 else 2 ** (depth - i) - 1
                if j < len(line) - 1:
                    print(sep * interval, end='')
            index += offset
            print()


    @classmethod
    def merge_sort(cls,array):
        """
        归并排序
        :param array: 排序数组
        :return:
        """
        if len(array) <= 1:
            return array
        middle  = int(len(array)/2)
        left = cls.merge_sort(array[:middle])
        right = cls.merge_sort(array[middle:])
        return list(merge(left,right))

    @classmethod
    def merge(cls,left,right):
        """
        归并两个有序序列
        :param left:
        :param right:
        :return:
        """
        result = []
        append =result.append
        l,r=0,0
        while l < len(left) and len(right)> r:
            if left[l] < right[r]:
                append(left[l])
                l +=1
            else:
                append(right[r])
                r +=1
        result += list(left[l:])
        result += list(right[r:])
        return result

if __name__ == '__main__':
    myList = [49, 38, 65, 97, 76, 13, 27,49,53,78]
    print("Quick Sort: ")
    print(SortTools.quick_sort(myList))
    print("Selection Sort: ")
    myList = [49, 38, 65, 97, 76, 13, 27, 49, 53, 78]
    SortTools.selection_sort(myList)
    print(myList)
    myList = [49, 38, 65, 97, 76, 13, 27, 49, 53, 78]
    print("Heap Sort: ")
    myList = [49, 38, 65, 97, 76, 13, 27, 49, 53, 78]
    print(SortTools.heap_sort(myList))
    # SortTools.print_tree(myList)
    print("Insertion Sort: ")
    myList = [49, 38, 65, 97, 76, 13, 27, 49, 53, 78]
    SortTools.insertion_sort(myList)
    print(myList)
    print("Merge Sort: ")
    myList = [49, 38, 65, 97, 76, 13, 27, 49, 53, 78]
    print(SortTools.merge_sort(myList))
