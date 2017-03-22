from django.shortcuts import render, redirect, get_object_or_404
from .forms import SearchForm
from .models import GeneFamily, Genes, Species, Alignment, AlignedSequence, GeneHasExpression


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
            seq = ""
            data =""
            family = GeneFamily.objects.get(gene_family_name=item)
            alignment = get_object_or_404(Alignment, gene_family_idgene_family=family.idgene_family)
            sequences = AlignedSequence.objects.filter(genes_idgenes__gene_family_idgene_family=family.idgene_family).select_related()
            ghexp = GeneHasExpression.objects.filter(genes_idgenes__gene_family_idgene_family=family.idgene_family).select_related()
            for sequence in sequences:
                seq += ">"+sequence.genes_idgenes.ensembl_id+"\n"+sequence.sequence+"\n"
            for exp in ghexp:
                organ = exp.organs_idorgans.organ_name
                subcondition = exp.conditions_idconditions.subcondition
                type_subcdition = exp.conditions_idconditions.subcondition_type
                type_cond = exp.conditions_idconditions.condition_type
                method = exp.expression_method_idexpression_method.quantification_tool
                typeexp = exp.expression_method_idexpression_method.expression_method_name
                explvl = exp.expressionlevel_idexpressionlevel.expression_level
                length = exp.expressionlevel_idexpressionlevel.length
                eff_count = exp.expressionlevel_idexpressionlevel.eff_count
                est_count = exp.expressionlevel_idexpressionlevel.est_count
                geneexp = exp.genes_idgenes.ensembl_id
                data += str(geneexp)+"\t"+str(length)+"\t"+str(eff_count)+"\t"+str(est_count)+"\t"+str(explvl)+"\n"
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
    return render(request, 'research/results.html', locals())
