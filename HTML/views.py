from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import SearchForm
from .models import GeneFamily, Genes, Species, Alignment, Expressionlevel, AlignedSequence


def search_data(request):
    # TODO : documentation
    """
    Form to search a :
        - gene family
        - gene name
        - gene Ensembl ID

    :param request:
    :return: render index.html
    """
    form = SearchForm(request.GET or None)
    if form.is_valid():
        item = form.cleaned_data['search']
        type_gene = form.cleaned_data['type']
        return redirect(results, item, type_gene)
    return render(request, 'research/index.html', locals())


def results(request, item, typedata):
    # TODO: documentation
    """
    :param request:
    :param item:
    :param typedata:
    :return:
    """
    if typedata == 'Gene family name':
        try:
            family = GeneFamily.objects.get(gene_family_name=item)
            alignment = get_object_or_404(Alignment, gene_family_idgene_family=family.idgene_family)
            genes = Genes.objects.filter(gene_family_idgene_family=family.idgene_family)
            sequence = AlignedSequence.objects.filter(genes_idgenes=genes)
        except GeneFamily.DoesNotExist:
            return render(request, 'research/Unknown.html', locals())
    elif typedata == 'Gene Ensembl ID':
        try:
            genes = Genes.objects.get(ensembl_id=item)
        except Genes.DoesNotExist:
            return render(request, 'research/Unknown.html', locals())
    elif typedata == 'Gene name':
        try:
            genes = Genes.objects.get(genes_name=item)
        except Genes.DoesNotExist:
            return render(request, 'research/Unknown.html', locals())
    else:
        try:
            species = Species.objects.get(species_name=item)
        except Species.DoesNotExist:
            return render(request, 'research/Unknown.html', locals())
    return render(request, 'research/Tree.html', locals())


def tree(request):
    return render(request, 'research/Tree.html', locals())


def expr(request, item):
    # exemple pour tooth 3
    try:
        expressionlevel = Expressionlevel.objects.all()
        geneid = Genes.objects.get(ensembl_id=item)
    except Expressionlevel.DoesNotExist:
        return render(request, 'research/Unknown.html', locals())
    tooth3 = open("Tooth3.html", "r")
    texte = tooth3.read()
    return HttpResponse(texte)
