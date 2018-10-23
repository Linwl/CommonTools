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

    def has_left_child(self):
        """
        是否有左子树
        :return:
        """
        return True if self.left else False

    def has_right_child(self):
        """
        是否有右子树
        :return:
        """
        return True if self.right else False

    def is_left_child(self):
        """
        是否左子树
        :return:
        """
        return self.parent and self.parent.left == self

    def is_right_child(self):
        """
        是否右子树
        :return:
        """
        return self.parent and self.parent.right == self


class BinarySearchTree:
    """
    二叉查找树
    """

    def __init__(self,root:TreeNode):
        self.root = root
        self.size = 0

    def length(self):
        """
        获取二叉树孩子个数
        :return:
        """
        return self.size

    def find(self,find_node):
        '''
        递归查找节点二叉树
        :param tree: 二叉树
        :param find_node: 查找节点
        :return:
        '''
        if not self.root:
            return None
        if self.root.node == find_node:
            return self.root
        elif find_node < self.root.node:
            return self.__find_node(self.root.left,find_node)
        elif find_node > self.root.node:
            return self.__find_node(self.root.right, find_node)

    def __find_node(self,tree,find_node):
        """
        递归查找节点树
        :param tree:
        :param find_node:
        :return:
        """
        if not tree:
            return None
        if tree.node == find_node:
            return tree
        elif find_node < tree.node:
            return self.__find_node(tree.left, find_node)
        elif find_node > tree.node:
            return self.__find_node(tree.right, find_node)

    def find_minimun(self,min=None):
        """
        查找最小单元
        :return:
        """
        if not min:
            min = self.root
        return self.__find_subtree(min)

    def find_maximun(self,max =None):
        """
        查找最大单元
        :return:
        """
        if not max:
            max = self.root
        return self.__find_subtree(max,direction ='RIGHT')

    def __find_subtree(self,tree,direction ='LEFT'):
        """
        查找最大或最小二叉子树
        :param tree:
        :param direction: LEFT RIGHT
        :return:
        """
        if direction == 'LEFT':
            while tree.left:
                tree = tree.left
            return tree
        elif direction == 'RIGHT':
            while tree.right:
                tree = tree.right
            return tree

    def insert_node(self,node):
        """
        二叉树插入
        :param node: 插入的节点
        :return:
        """
        tree = TreeNode(node=node)
        if not self.root:
            self.root = tree
            self.size = 0
        else:
            cur_node  = self.root
            while True:
                if tree.node < cur_node.node:
                    if cur_node.left:
                        cur_node = cur_node.left
                    else:
                        cur_node.left = tree
                        tree.parent = cur_node
                        self.size += 1
                        break
                elif tree.node > cur_node.node:
                    if cur_node.right:
                        cur_node = cur_node.right
                    else:
                        cur_node.right = tree
                        tree.parent = cur_node
                        self.size += 1
                        break
                else:
                    break

    def del_node(self,node):
        """
        删除二叉树节点
        :param node:指定二叉树节点
        :return:
        """
        del_tree = self.find(node)
        if not del_tree.has_left_child() and not del_tree.has_right_child():
            # 删除的节点为树叶,直接删除
            if del_tree == del_tree.parent.left:
                del_tree.parent.left = None
            else:
                del_tree.parent.right = None

        elif del_tree.has_left_child() and del_tree.has_right_child():
            # 有两个孩子
            min_tree = self.find_minimun(del_tree.right)
            min_tree.parent = del_tree.parent
            min_tree.right = del_tree.right
            min_tree.left = del_tree.left
        else:
            # 只有一个子树
            parent = del_tree.parent
            if del_tree.has_left_child():
                # 拥有左子树
                subtree = del_tree.left
                self.__handle_child(del_tree, parent, subtree)
            elif del_tree.has_right_child():
                #拥有右子树
                subtree = del_tree.right
                self.__handle_child(del_tree, parent, subtree)

    def __handle_child(self, del_tree, parent, subtree):
        """
        处理左右子树节点
        :param del_tree:
        :param parent:
        :param subtree:
        :return:
        """
        if del_tree.is_left_child():
            # 删除节点是左子树
            parent.left = subtree
            subtree.parent = parent
        elif del_tree.is_right_child():
            # 删除节点是右子树
            parent.right = subtree
            subtree.parent = parent
        else:
            # 是根
            self.__handle_root(subtree.left)

    def __handle_root(self, subtree):
        '''
        处理根节点
        :param subtree:
        :return:
        '''
        self.root = subtree
        subtree.parent = None
        subtree = None


if __name__ == '__main__':
    tree = TreeNode(5)
    bintree=BinarySearchTree(tree)
    bintree.insert_node(1)
    bintree.insert_node(3)
    bintree.insert_node(6)
    bintree.insert_node(7)
    print(bintree)
    print(bintree.find_minimun().node)
    print(bintree.find_maximun().node)

