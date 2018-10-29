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
from  collections import deque

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

class Graph(object):
    """
    图类
    """

    def __init__(self, *args, **kwargs):
        self.node_neighbors = {}
        self._queue = deque()
        self.orders = []

    def add_nodes(self, nodelist):
        """
        增加节点
        :param nodelist:
        :return:
        """
        if isinstance(nodelist,list):
            if(len(nodelist) >0):
                for node in nodelist:
                    self.__add_node(node)
            else:
                raise ValueError('nodelist is empty!')
        else:
            raise ValueError('nodelist is not list!')

    def __add_node(self, node):
        if not node in self.nodes():
            self.node_neighbors[node] = []

    def add_edge(self, edge):
        """
        增加图的边坐标
        :param edge:
        :return:
        """
        u, v = edge
        if (v not in self.node_neighbors[u]) and (u not in self.node_neighbors[v]):
            self.node_neighbors[u].append(v)
            if (u != v):
                self.node_neighbors[v].append(u)

    def nodes(self):
        return self.node_neighbors.keys()

    def bfs(self,root):
        """
        广度优先搜索
        :param root:
        :return:
        """
        self._init_fs(root)
        while len(self._queue):
            person = self._queue.popleft()
            if (not person in self.visited) and (person in self.node_neighbors.keys()):
                self._queue += self.node_neighbors[person]
                self.v_append(person)
                self.or_append(person)

    def dfs(self,root):
        """
        深度优先搜索
        :param root:
        :return:
        """
        self._init_fs(root)
        while len(self._queue):
            person = self._queue.popleft()
            if (not person in self.visited) and (person in self.node_neighbors.keys()):
                temp = self.node_neighbors[person]
                temp.reverse()
                for index in temp:
                    self._queue.appendleft(index)
                self.v_append(person)
                self.or_append(person)

    def _init_fs(self,root):
        if root:
            self.visited = []
            self.or_append = self.orders.append
            self.v_append = self.visited.append
            if root in self.node_neighbors.keys():
                self._queue.append(root)
            else:
                self.or_append(-1)
                return
        else:
            raise ValueError('root is None')



    def clear(self):
        self.orders = []

    def node_print(self):
        for index in self.orders:
            print(index, end='  ')


if __name__ == '__main__':
    # arry = [4,5,9,3,1,7]
    # print(binary_search(arry,4))
    # print(interpolation__search(arry, 4))
    g = Graph()
    g.add_nodes([i for i in range(1,9)])
    g.add_edge((1, 2))
    g.add_edge((1, 3))
    g.add_edge((2, 4))
    g.add_edge((2, 5))
    g.add_edge((3, 6))
    g.add_edge((3, 7))
    g.add_edge((6, 7))
    g.add_edge((4, 8))
    g.add_edge((5, 8))
    print("nodes:", g.nodes())
    g.bfs(1)
    print('BFS:')
    print('  ', end='  ')
    g.node_print()
    g.clear()
    print()
    print('DFS:')
    print('  ', end='  ')
    g.dfs(1)
    g.node_print()