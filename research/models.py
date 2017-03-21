""" This is the Django models file.
   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
 Feel free to rename the models, but don't rename db_table values or field names.
"""
from __future__ import unicode_literals

from django.db import models


class GeneFamily(models.Model):
    idgene_family = models.AutoField(primary_key=True)
    gene_family_name = models.CharField(unique=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'gene_family'


class Species(models.Model):
    idspecies = models.AutoField(primary_key=True)
    species_name = models.CharField(unique=True, max_length=45)
    species_taxid = models.CharField(db_column='Species_Taxid', unique=True, max_length=45, blank=True, null=True)  # Field name made lowercase.
    assembly_name = models.CharField(db_column='Assembly_name', max_length=45, blank=True, null=True)  # Field name made lowercase.
    assembly_source = models.CharField(db_column='Assembly_source', max_length=45, blank=True, null=True)  # Field name made lowercase.
    species_classification = models.TextField(db_column='Species_Classification', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'species'


class Alignment(models.Model):
    idalignment = models.AutoField(primary_key=True)  # Field name made lowercase.
    tree = models.TextField()
    gene_family_idgene_family = models.ForeignKey('GeneFamily', models.DO_NOTHING, db_column='gene_family_idgene_family')

    class Meta:
        managed = False
        db_table = 'Alignment'
        unique_together = (('idalignment', 'gene_family_idgene_family'),)


class Conditions(models.Model):
    idconditions = models.AutoField(primary_key=True)
    dvp_stage = models.CharField(max_length=45, blank=True, null=True)
    subcondition = models.CharField(max_length=45)
    condition_type = models.CharField(max_length=45, blank=True, null=True)
    subcondition_type = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'conditions'
        unique_together = (('dvp_stage', 'subcondition', 'condition_type', 'subcondition_type'),)


class ExpressionMethod(models.Model):
    idexpression_method = models.AutoField(primary_key=True)
    expression_method_name = models.CharField(max_length=45)
    quantification_tool = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expression_method'
        unique_together = (('expression_method_name', 'quantification_tool'),)


class Expressionlevel(models.Model):
    idexpressionlevel = models.AutoField(primary_key=True)
    length = models.IntegerField()
    eff_count = models.FloatField()
    est_count = models.IntegerField()
    expression_level = models.FloatField()

    class Meta:
        managed = False
        db_table = 'expressionlevel'


class Organs(models.Model):
    idorgans = models.AutoField(primary_key=True)
    organ_name = models.CharField(unique=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'organs'


class AlignedSequence(models.Model):
    idaligned_sequence = models.AutoField(primary_key=True)
    sequence = models.TextField()
    alignment_idalignment = models.ForeignKey(Alignment, models.DO_NOTHING, db_column='Alignment_idAlignment')  # Field name made lowercase.
    genes_idgenes = models.ForeignKey('Genes', models.DO_NOTHING, db_column='genes_idgenes')

    class Meta:
        managed = False
        db_table = 'aligned_sequence'
        unique_together = (('idaligned_sequence', 'alignment_idalignment'),)


class Genes(models.Model):
    idgenes = models.AutoField(primary_key=True)
    genes_name = models.CharField(max_length=45)
    ensembl_id = models.CharField(db_column='Ensembl_ID', unique=True, max_length=45)  # Field name made lowercase.
    gene_family_idgene_family = models.ForeignKey(GeneFamily, models.DO_NOTHING, db_column='gene_family_idgene_family')
    species_idspecies = models.ForeignKey('Species', models.DO_NOTHING, db_column='species_idspecies')

    class Meta:
        managed = False
        db_table = 'genes'


class GeneHasExpression(models.Model):
    idgene_has_expressioncol = models.AutoField(primary_key=True)
    genes_idgenes = models.ForeignKey('Genes', on_delete=models.CASCADE, db_column='genes_idgenes')
    expressionlevel_idexpressionlevel = models.ForeignKey(Expressionlevel, on_delete=models.CASCADE, db_column='expressionlevel_idexpressionlevel')
    expression_method_idexpression_method = models.ForeignKey(ExpressionMethod, on_delete=models.CASCADE, db_column='expression_method_idexpression_method')
    conditions_idconditions = models.ForeignKey(Conditions, on_delete=models.CASCADE, db_column='conditions_idconditions')
    organs_idorgans = models.ForeignKey('Organs', on_delete=models.CASCADE, db_column='organs_idorgans')

    class Meta:
        managed = False
        db_table = 'gene_has_expression'
        unique_together = (('idgene_has_expressioncol', 'genes_idgenes', 'expressionlevel_idexpressionlevel', 'expression_method_idexpression_method', 'conditions_idconditions', 'organs_idorgans'),)

