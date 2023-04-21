class TreeNode:
    """
    A class of Tree node

    Attributes
    ----------
    left: left node
    right: right node
    data: contains all the info of the current node
    """
    def __init__(self, data):
        """
        initialze a tree node with input data

        Param:
        data: dictionary, contains info of championId championLevel championpoitns
        """
        self.left = None
        self.right = None
        self.data = data

class BST:
    """
    A class of binray search tree

    Attributes
    ----------
    root: the root of the BST, it should be a tree node
    """
    def __init__(self):
        """
        initialze a binary tree with root node is None
        """
        self.root = None

    def insert(self, data):
        """
        Insert a node into binray search tree

        Param:
        data: dictionary, contains info of the new node
        """
        if self.root is None:
            self.root = TreeNode(data)
        else:
            self.insert_nodes(data, self.root)

    def insert_nodes(self, data, current_node):
        """
        helper function of inser. Insert a node into binray search tree at the correct position

        Param:
        data: dictionary, contains info of the new node
        current_node: Treenode(), insert to its left or right
        """
        if data['championPoints'] < current_node.data['championPoints']:
            if current_node.left is None:
                current_node.left = TreeNode(data)
            else:
                self.insert_nodes(data, current_node.left)
        elif int(data['championPoints']) > int(current_node.data['championPoints']):
            if current_node.right is None:
                current_node.right = TreeNode(data)
            else:
                self.insert_nodes(data, current_node.right)
        else:
            # duplicate, do nothing
            pass

    def find(self, ID):
        """
        Find and return the node with provided ID num

        Param:
        ID: int, the champoion's id which user want to find
        """
        if self.root is not None:
            return self.find_temp(ID, self.root)
        else:
            return None

    def find_temp(self, ID, current_node):
        """
        helper function of find. Find and return the node with provided ID num
        call recursively until find the ID

        Param:
        ID: int, the champoion's id which user want to find
        current_node: TreeNode(), check its left and righ node
        """
        if current_node is None:
            return None
        if ID == current_node.data['championId']:
            print(current_node.data)
            return current_node.data
        else:
            left_result = self.find_temp(ID, current_node.left)
            if left_result is not None:
                return left_result
            else:
                return self.find_temp(ID, current_node.right)


    def get_min_value(self):
        """
        return the node with the min champion's points

        Param:
        None
        """
        if self.root is None:
            return None
        else:
            return self.min_value(self.root)

    def min_value(self, current_node):
        """
        helper function of get_min_valie, return the node with the min champion's points

        Param:
        current_node: TreeNode(), current node used to check if its the min
        """
        if current_node.left is None:
            return current_node.data
        else:
            return self.min_value(current_node.left)

    def get_max_value(self):
        """
        return the node with the max champion's points

        Param:
        None
        """
        if self.root is None:
            return None
        else:
            return self.max_value(self.root)

    def max_value(self, current_node):
        """
        helper function of get_min_valie, return the node with the min champion's points

        Param:
        current_node: TreeNode(), current node used to check if its the max
        """
        if current_node.right is None:
            return current_node.data
        else:
            return self.max_value(current_node.right)
    
    def count_nodes_greater_than_root(self):
        """
        count the number of champions that have greater champio's points that the root champion

        Param:
        none
        """
        return self.count_greater_than_root_helper(self.root.right, self.root.data)

    def count_greater_than_root_helper(self, node, data):
        """
        helper function of count_nodes_greater_than_root, 
        count the number of champions that have greater champio's points that the root champion

        Param:
        node:TreeNode0(), check if its champion points is larger than root champion
        data:dictionary, contains data of the root node
        """
        if node is None:
            return 0
        elif node.data['championPoints'] > data['championPoints']:
            return 1 + self.count_greater_than_root_helper(node.left, data) + self.count_greater_than_root_helper(node.right, data)
        else:
            return self.count_greater_than_root_helper(node.right, data)

    def count_nodes_smaller_than_root(self):
        """
        count the number of champions that have lower champio's points that the root champion

        Param:
        none
        """
        return self.count_smaller_than_root_helper(self.root.left, self.root.data)

    def count_smaller_than_root_helper(self, node, data):
        """
        helper function of count_nodes_smaller_than_root, 
        count the number of champions that have smaller champio's points that the root champion

        Param:
        node:TreeNode0(), check if its champion points is smaller than root champion
        data:dictionary, contains data of the root node
        """
        if node is None:
            return 0
        elif node.data['championPoints'] < data['championPoints']:
            return 1 + self.count_smaller_than_root_helper(node.left, data) + self.count_smaller_than_root_helper(node.right, data)
        else:
            return self.count_smaller_than_root_helper(node.left, data)