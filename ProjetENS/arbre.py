from ete3 import Tree, faces, TreeStyle
import utils
from numpy import random

essai_arbre = "((((((ENSMUSP00000140794_F10789:99,ENSMUSP00000140064_F10789:0)10:0,ENSMUSP00000140067_F10789:0.001506)1:0,ENSMUSP00000140105_F10789:0)1:0,ENSMUSP00000139400_F10789:0)1:0.001505,ENSMUSP00000141092_F10789:0)1:0.22726,ENSMUSP00000112771_F10789:0.23027);"
# Reading tree t1 and t2
t = Tree(essai_arbre)
print(t)


def mylayout(node):
    if node.is_leaf():
        pass
    # If node is a duplication node

    else:
        # Set the style as a red circle
        node.img_style["size"] = 6
        node.img_style["shape"] = "circle"
        node.img_style["fgcolor"] = "red"


# And, finally, display the tree using the layout function
ts = TreeStyle()
ts.show_leaf_name = False
ts.layout_fn = mylayout(t)
t.render("tree4.png", dpi=600, tree_style=ts)
