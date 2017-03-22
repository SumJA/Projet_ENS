source("http://bioconductor.org/biocLite.R")
biocLite("biomaRt")

library(biomaRt)

listEnsembl(version=87)
ensembl = useEnsembl(biomart="ensembl",version=87)



# Test sur la souris
lDatasets = listDatasets(ensembl)
head(listDatasets(ensembl))

ensembl87_Mmusculus = useEnsembl(biomart="ensembl",version=87, dataset="mmusculus_gene_ensembl")

lFilters = listFilters(ensembl87_Mmusculus)
head(lFilters)
lAttributes = listAttributes(ensembl87_Mmusculus, page = "feature_page")
head(lAttributes)


all_genes_mus = getBM(attributes=c('ensembl_gene_id',
                               'ensembl_peptide_id',
                               "gene_biotype",
                               "mgi_id", "ucsc",
                               "external_gene_name", "description"
                               #, "go_id", "name_1006"
                               ),
                  filters = c("transcript_biotype"), values = c("protein_coding"),
                  mart = ensembl87_Mmusculus)

head(all_genes_mus)


write.table(all_genes_mus, "table_equivalence_mus.tsv", quote=F, row.names = F , sep = "\t")


# Création de la table pour toutes les espèces dispo

f <- function(dataset_l) {

  dataset = dataset_l["dataset"]
  print(dataset)
  
  ensembl87 = useEnsembl(biomart="ensembl",version=87, dataset=dataset)
  all_genes = getBM(attributes=c('ensembl_gene_id',
                                 'ensembl_peptide_id',
                                 "gene_biotype",
                                 "external_gene_name", "description"
                                 #, "go_id", "name_1006"
  ),
  filters = c("transcript_biotype"), values = c("protein_coding"),
  mart = ensembl87)
  all_genes$dataset = dataset
  all_genes$species = gsub("_gene_ensembl","", dataset)
  all_genes$dataset_description =  dataset_l["description"]
  return(all_genes)
}

l_all_genes = apply(lDatasets,1,f)

library(plyr)
all_genes = ldply(l_all_genes)[,-1]

#all_genes = do.call("rbind", l_all_genes )

write.table(all_genes, "table_equivalence.tsv", quote=F, row.names = F, sep = "\t")


