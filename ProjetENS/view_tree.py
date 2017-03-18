from django.shortcuts import render
from django.http import HttpResponse
from ete3 import Tree, faces, TreeStyle
from django import forms


# from appTest import left_menu


#
# import utils
# from menu import *


# Create your views here.

# def index(request):
#    return HttpResponse(view_tree())


def view_tree():
    # text = """<h2>This is the tree ! </h2>"""
    tree_file = open("F00000.tree", "r")
    for line in tree_file.readlines():
        tree = line
        t2 = Tree(tree)
    # t2 = t2.get_ascii().replace("\n", "<br/>").replace(" ", "&nbsp;")
    #    menu = left_menu.menu()
    print(t2)
