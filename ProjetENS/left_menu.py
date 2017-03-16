from django.shortcuts import render
from django.http import HttpResponse


def menu():
    menu = """<ul id="navigation">
		<li><a href="#" title="See the expression data">Expression</a></li>
		<li><a href="#" title="See the alignment">Alignment</a></li>
		<li><a href="#" title="See the tree">Tree</a></li>
		<li><a href="#" title="See all data">All</a></li>
		</ul>"""
    return menu
