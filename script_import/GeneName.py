def recup_name(file):
    i = 0
    dict_gene = {}
    dict_pept = {}
    for line in file:
        liste = line.split("\t")
        if i == 0:  # remove the first line : name of column
            i += 1
        else:
            id_gene = liste[0]
            id_pept = liste[1]
            gene_name = liste[5]
            dict_gene[id_gene] = gene_name
            dict_pept[id_pept] = gene_name


# Je t'ai fais plusieurs solution parce que je savaias pas ce qui était le mieux pour toi


# For mus_musculus
file_mus = open("table_equivalence_mus.tsv", "r")
recup_name(file_mus)

# for all species
# file_all = open("table_equivalence.tsv", "r")
# recup_name(file_all)
