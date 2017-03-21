import os
from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Alignment, AlignedSequence
from .make_tree import show_tree


def get_tree(request):
    family_id = 58997
    alignment = get_object_or_404(Alignment, gene_family_idgene_family=family_id)
    view_tree = show_tree(alignment.tree)
    # return render(request, 'dataViewer/tree.html', {'view_tree': view_tree})
    return HttpResponse(view_tree)


def get_alignment(request):
    aligned_sequence = ""
    family_name = 'F00000'
    file = os.path.join(os.path.join('/home/sumaira/Documents/Projet2/données/ProjetM1BioInfo/Version1', "Alignments"), family_name + ".fasta")
    f = open(file, "r")
    for line in f:
        aligned_sequence += line
    return render(request, 'dataViewer/alignment.html', locals())
