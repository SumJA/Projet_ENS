Introduction :

We have data on gene families. For each gene, we have data about genes alignments, genes tree ans genes expression.
In this web application, we group all this data. This website makes it possible to visualize all the data, for a gene
or for a family.

For this project, you need to have a python version superior to 3.4.

I Data Base
 1. Tables

Genes : PRIMARY KEY idgenes, genes_name, Ensembl_ID, #species_idspecies, #gene_family_idgene_family
Genes_family : PRIMARY KEY idgene_family, gene_family_name
Expressionlevel : PRIMARY KEY idexpressionlevel, length, eff_count, est_count, expression_level
Expression_method : PRIMARY KEY idexpression_method, expression_method_name, quantification_tool
Gene_has_expression : PRIMARY KEY idgene_has_expression, #gene_idgenes, #expressionlevel_idexpressionlevel, #expression_method_idimpression_method, #conditions_idconditions, #organs_idorgans
Organs : PRIMARY KEY idorgans, organ_name
Alignment (TREE) : PRIMARY KEY idAlignment, tree, #gene_family_idgene_family
Aligned_sequences : PRIMARY KEY idaligned_sequence, sequence, #Alignment_idAlignment, #genes_idgenes
Conditions : PRIMARY KEY idconditions, subcondition, condition_type, subcondition_type
Species : PRIMARY KEY idspecies, species_name, species_Taxid, assembly_name, assembly_source, species_Classification

In bddsqlsql.sql : script for creation of the database
In Database/data : script for the insertion of datas in the data base.


 2. How to import data

In script_import/argparser.py : Arguments for importing the data

If you want to complete the database, the format of the datas must to respect the same format of our datas. 

II Django

 1. Installation

sudo apt-get install python3-pip
sudo aptitude install python3-django
sudo pip install django

OR

pip install Django==1.10


 2. Utilization

You just need to parameterize the database in /ProjetENS/settings.py.
Now, to visualize the web site, you need to run (in a local server) the file view.py
who is in research folder.

DANS DJANGO LANCER LE FICHIER VIEW.PY


III Data visualization
All this part are do in JavaScript. All that you need to execute this visualization is include in the differents
scripts.

 1. Expression
You can see the expressions in various histogram. There is a graph for eatch organ and condition. In the y axes,
you have the ensembl's identifiant of all genes that have an expression in the same organ and condition as the genes
that you search.

 2. Alignment
Inut : format fasta

 3. Tree
Input : format newick
