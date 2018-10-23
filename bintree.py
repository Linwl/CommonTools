#!usr/bin/env python
# coding=utf-8

"""
@company:广东浩迪创新科技有限公司
@version: ??
@author: linwl
@file: bintree.py
@time: 2018/10/23 9:53
@function：二叉查找树实现算法
"""

class TreeNode:
    """
    二叉树结构类
    """

    def __init__(self, node,left=None,right=None,parent=None):
        self.node = node
        self.parent = parent
        self.left = left
        self.right = right

class BinarySearchTree:
    """
    二叉查找树
    """

    def __init__(self):
        self.root = None
        self.size = 0

    def length(self):
        return self.size

    def find(self,tree,find_node):
        '''
        递归查找
        :param tree: 二叉树
        :param find_node: 查找节点
        :return:
        '''
        if not tree:
            return None
        if tree.node == find_node:
            return tree
        elif find_node < tree.node:
            return self.find(tree.left,find_node)
        elif find_node > tree.node:
            return self.find(tree.right, find_node)

    def find_minimun(self,tree):
        """
        查找最小单元
        :param tree: 二叉树
        :return:
        """
        min = tree
        if tree:
            while not min.left:
                min = min.left
            return min
        else:
            return None

    def find_maximun(self, tree):
        """
        查找最大单元
        :param tree: 二叉树
        :return:
        """
        min = tree
        if tree:
            while not min.right:
                min = min.right
            return min
        else:
            return None

    def insert_tree(self,node):
        """
        二叉树插入
        :param node: 插入的节点
        :return:
        """
        tree = TreeNode(node=node)
        if not self.root:
            self.root = tree
            self.size += 1
        else:
            cur_node = self.root
            if node < cur_node.node:
                self.insert_tree()
