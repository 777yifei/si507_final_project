from BST import TreeNode
import json

def dict_to_bst(data):
    """
    read a dictionary and return a BST based on those data

    Param:
    data: dictionary, contains data of a binary search tree
    """
    if not data:
        return None
    node = TreeNode(data)
    node.left = dict_to_bst(data.get('left'))
    node.right = dict_to_bst(data.get('right'))
    return node

with open('tree.json', 'r') as f:
    bst_dict = json.load(f)

binary_tree = dict_to_bst(bst_dict)