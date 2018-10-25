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
import queue

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
        非递归查找节点二叉树
        :param tree: 二叉树
        :param find_node: 查找节点
        :return:
        '''
        bt = self.root
        while bt:
            cur_node = bt.node
            if find_node < cur_node:
                bt = bt.left
            elif find_node > cur_node:
                bt = bt.right
            else:
                return bt
        return None

    def recursion_find(self,find_node):
        """
        递归查找二叉树节点
        :param find_node: 查找节点
        :return:
        """
        if not self.root:
            return None
        if self.root.node == find_node:
            return self.root
        elif find_node < self.root.node:
            return self.__find_node(self.root.left, find_node)
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
        if del_tree:
            if not del_tree.has_left_child() and not del_tree.has_right_child():
                # 删除的节点为树叶,直接删除
                if del_tree == del_tree.parent.left:
                    del_tree.parent.left = None
                else:
                    del_tree.parent.right = None
            elif del_tree.has_left_child() and del_tree.has_right_child():
                # 有两个孩子
                min_tree = self.find_minimun(del_tree.right)
                # 再把右子树中最小值节点删除
                self.del_node(min_tree.node)
                del_tree.node = min_tree.node
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
        else:
            return None

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

    def preorder_print_tree(self,tree):
        """
        前序打印二叉查找树
        :return:
        """
        stack = [tree]
        append = stack.append
        print('前序遍历:')
        while len(stack) > 0:
            print(tree.node,end='->')
            if tree.right:
                append(tree.right)
            if tree.left:
                append(tree.left)
            tree = stack.pop()

    def inorder_print_tree(self,tree):
        """
        中序遍历打印二叉查找树
        :param tree: 二叉查找树
        :return:
        """
        stack =[]
        append = stack.append
        pos =tree
        pop = stack.pop
        print('中序遍历:')
        while pos or len(stack)>0:
            if pos:
                append(pos)
                pos = pos.left
            else:
                pos = pop()
                print(pos.node,end='->')
                pos = pos.right

    def postorder_print_tree(self,tree):
        """
        后序遍历打印二叉查找树
        :param tree: 二叉查找树
        :return:
        """
        stack = [tree]
        stack2 = []
        append1 = stack.append
        append2 = stack2.append
        print('后序遍历:')
        while len(stack)>0:
            node = stack.pop()
            append2(node)
            if node.left:
                append1(node.left)
            if node.right:
                append1(node.right)
        while len(stack2)>0:
            print(stack2.pop().node,end='->')

    def layer_traverse_print_tree(self,tree):
        """
        层序打印二叉查找树
        :param tree:
        :return:
        """
        if not tree:
            return None
        que = queue.Queue()  # 创建先进先出队列
        que.put(tree)
        print('层序遍历:')
        while not que.empty():
            head = que.get()  # 弹出第一个元素并打印
            print(head.node,end='->')
            if head.left:  # 若该节点存在左子节点,则加入队列（先push左节点）
                que.put(head.left)
            if head.right:  # 若该节点存在右子节点,则加入队列（再push右节点）
                que.put(head.right)




if __name__ == '__main__':
    tree = TreeNode(7)
    bintree=BinarySearchTree(tree)
    bintree.insert_node(3)
    bintree.insert_node(2)
    bintree.insert_node(5)
    bintree.insert_node(6)
    bintree.insert_node(4)
    bintree.insert_node(9)
    bintree.insert_node(8)
    bintree.insert_node(10)
    bintree.preorder_print_tree(bintree.root)
    print()
    bintree.inorder_print_tree(bintree.root)
    print()
    bintree.postorder_print_tree(bintree.root)
    print()
    bintree.layer_traverse_print_tree(bintree.root)
    # print(bintree.find_minimun().node)
    # print(bintree.find_maximun().node)
    # bintree.del_node(3)


