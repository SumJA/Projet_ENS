"""
This script generates a PhyloTree
"""
from ete3 import Tree


def show_tree(tree):
    """
    Tree visualisation
    :param tree:
    :param alignment:
    :return: None
    """
    # Visualize the tree
    t2 = Tree(tree)
    t2 = t2.get_ascii().replace("\n", "<br/>").replace(" ", "&nbsp;")
    return t2


