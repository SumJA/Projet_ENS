from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse(view_alignment())


def view_alignment():
    alignment_file = open("F00000.fasta", "r")
    for line in alignment_file.readlines():
        alignment = line
    return alignment
