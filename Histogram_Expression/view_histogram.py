from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def index(request):
    # exemple pour tooth 3
    tooth3 = open("Tooth3.html", "r")
    texte = tooth3.read()
    return HttpResponse(texte)
