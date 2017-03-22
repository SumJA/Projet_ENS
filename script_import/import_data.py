import mysql.connector
import os
from mysql.connector import errorcode
from script_import import get_data
from script_import import config_db
from colorama import Fore  # color console module

path_directory = get_data.path_directory
exp_filename = get_data.file_name
species_metadata_file = get_data.species_file
database_configuration = config_db.config


class ImportData:
    # TODO : des commit regroupés !!!!
    # TODO : complete doc
    """A data importer :
            Extract then Import the data from a file containing all :
                - the alignments information
                - phylogenetic trees
                - level of expression
                - information on the species_metadata_file analyzed
    """

    def __init__(self, path, config, expression_file):
        """
        :param path (str): Path to the data directory.
        :param config (dict): A dictionary with database _connexion information
        :param exp_filename (str): Name of the expression level file
        """
        self._get_data = get_data.GetData(path)
        self.expression_filename = expression_file
        self.families = self._get_data.extract_all_families()
        try:
            self._connexion = mysql.connector.connect(**config)
            self._cursor = self._connexion.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print(Fore.RED + "Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print(Fore.RED + "Database does not exist")
            else:
                print(Fore.RED + str(err))

    def import_families(self):
        """
        Imports all families in alignment directory.
        If you want to import only a specific family from the alignment directory, use the import_a_family method.

        :return: None
        """
        for fg in self.families.keys():
            add_family_name = """INSERT INTO gene_family(gene_family_name) VALUES ('%s');""" % fg
            try:
                print(Fore.GREEN + "Trying to insert family:", fg)
                self._cursor.execute(add_family_name)
            except mysql.connector.Error as err:
                print(Fore.RED + str(err))
                self._connexion.rollback()
            else:
                self._connexion.commit()

    def import_a_family(self, family: str):
        """
        Imports a family in the database.
        If you want to import all the families from the alignment directory, use the import_families method.

        :param family:
        :return:
        """
        add_family_name = """INSERT INTO gene_family(gene_family_name) VALUE ('%s')""" % family
        try:
            print(Fore.GREEN + "Trying to insert family:", family)
            self._cursor.execute(add_family_name)
        except mysql.connector.Error as err:
            print(Fore.RED + str(err))
            self._connexion.rollback()
        else:
            self._connexion.commit()

    def import_species(self, species_filename: str):
        """
        Imports all species from a species metadata file.

        :return: None
        """
        species = self._get_data.extract_all_species(species_filename)
        for i in species:
            sp_name = i[0]
            sp_taxid = i[1]
            asbly_name = i[2]
            asbly_source = i[3]
            sp_classification = i[4]
            select_species = """SELECT COUNT(*) FROM species WHERE species_name = '%s' and Species_Taxid = '%s'and Assembly_name = '%s' and Assembly_source ='%s' AND Species_Classification = '%s';""" % (sp_name, sp_taxid, asbly_name, asbly_source, sp_classification)
            add_species = """INSERT INTO species(species_name, Species_Taxid, Assembly_name, Assembly_source, Species_Classification) VALUES ('%s', '%s', '%s', '%s', '%s');""" % (sp_name, sp_taxid, asbly_name, asbly_source, sp_classification)
            try:
                self._cursor.execute(select_species)
                count = self._cursor.fetchone()[0]
            except mysql.connector.Error as err:
                print(Fore.RED + str(err))
                self._connexion.rollback()
            else:
                if count == 0:
                    try:
                        print(Fore.GREEN + "Trying to insert data for species :", sp_name)
                        self._cursor.execute(add_species)
                    except mysql.connector.Error as err:
                        print(Fore.RED + str(err))
                        self._connexion.rollback()
                    else:
                        self._connexion.commit()
                else:
                    print(Fore.RED + "Duplicate entry %s - The insert has been ignored" % i)

    def import_organs(self):
        """
        Imports organ information into organ table.
        If you want to import only the organs from the expression metadata file use this function. If you want to
        extract all the information from the file, use the import_organs_expression_method_condition function instead of
        this one.

        :return: None
        """
        # Extract information from file:
        conditions = self._get_data.extract_all_expression_info()
        for info in conditions:
            organ = info[0]
            add_organs = """INSERT INTO organs(organ_name) VALUES ('%s')""" % organ
            try:
                print(Fore.GREEN + "Trying to insert name for organ :", organ)
                self._cursor.execute(add_organs)
            except mysql.connector.Error as err:
                print(Fore.RED + str(err))
                self._connexion.rollback()
            else:
                self._connexion.commit()

    def import_expression_method(self):
        """
        Imports expression method information into expression_method table of the database.
        If you want to import only the expression method from the expression metadata file use this function.
        If you want to extract all the information from the file, use the import_organs_expression_method_condition
        function instead of this one.

        :return: None
        """
        # Extract information from file:
        conditions = self._get_data.extract_all_expression_info()
        for info in conditions:
            method_expr = info[1]
            tool = info[2]
            select_mthd = """SELECT COUNT(*) FROM expression_method WHERE expression_method_name = '%s' AND quantification_tool = '%s';""" % (method_expr, tool)
            add_method = """INSERT INTO expression_method(expression_method_name, quantification_tool) VALUES ('%s','%s')""" % (method_expr, tool)
            try:
                self._cursor.execute(select_mthd)
                count = self._cursor.fetchone()[0]
            except mysql.connector.Error as err:
                print(Fore.RED + str(err))
            else:
                if count == 0:
                    try:
                        print(Fore.GREEN + "Trying to insert expression method : ", method_expr, tool)
                        self._cursor.execute(add_method)
                    except mysql.connector.Error as err:
                        print(Fore.RED + str(err))
                        self._connexion.rollback()
                    else:
                        self._connexion.commit()
                else:
                    print(Fore.RED + "Duplicate entry '%s' - The insert has been ignored" % (method_expr + ", " + tool))

    def import_condition(self):
        """
        Imports experience conditions information into conditions table of the database.
        If you only want to import the experience conditions information from the expression metadata file use this
        function.
        If you want to extract all the information from the file, use the import_organs_expression_method_condition
        function instead of this one.

        :return:
        """
        # Extract information from file:
        conditions = self._get_data.extract_all_expression_info()
        for info in conditions:
            subcondition = info[3][0]
            cond_type = info[3][1]
            subcondition_type = info[3][2]
            # FIXME : dvp_stage à définir !
            # check for double NULL value :
            select_conditions = """SELECT COUNT(*) FROM conditions WHERE subcondition = '%s' and condition_type = '%s' and subcondition_type = '%s';""" % (
            subcondition, cond_type, subcondition_type)
            add_conditions = """INSERT INTO conditions(subcondition, condition_type, subcondition_type) VALUES ('%s', '%s', '%s')""" % (subcondition, cond_type, subcondition_type)
            try:
                self._cursor.execute(select_conditions)
                count = self._cursor.fetchone()[0]
            except mysql.connector.Error as err:
                print(Fore.RED + str(err))
                self._connexion.rollback()
            else:
                if count == 0:
                    try:
                        print(Fore.GREEN + "Trying to insert conditions infos:", info)
                        self._cursor.execute(add_conditions)
                    except mysql.connector.Error as err:
                        print(Fore.RED + str(err))
                        self._connexion.rollback()
                    else:
                        self._connexion.commit()
                else:
                    print(Fore.RED + "Duplicate entry '%s' - The insert has been ignored" % (subcondition + ", " + cond_type + ", " + subcondition_type))

    def import_organs_expression_method_condition(self):
        """
        Imports data in tables organs, expression_method and conditions.
        If you want to import all the information from the expression metadata file, use this function.

        :return: None
        """
        # Extract information from file:
        conditions = self._get_data.extract_all_expression_info()
        for info in conditions:
            organ = info[0]
            method_expr = info[1]
            tool = info[2]
            subcondition = info[3][0]
            cond_type = info[3][1]
            subcondition_type = info[3][2]
            add_organs = """INSERT INTO organs(organ_name) VALUES ('%s')""" % organ
            # FIXME : dvp_stage à définir !
            # verifier doublons avec null
            select_conditions = """SELECT COUNT(*) FROM conditions WHERE subcondition = '%s' and condition_type = '%s' and subcondition_type = '%s'""" % (subcondition, cond_type, subcondition_type)
            add_conditions = """INSERT INTO conditions(subcondition, condition_type, subcondition_type) VALUES ('%s', '%s', '%s')""" % (subcondition, cond_type, subcondition_type)
            select_mthd = """SELECT COUNT(*) FROM expression_method WHERE expression_method_name = '%s' AND quantification_tool = '%s';""" % (
            method_expr, tool)
            add_method = """INSERT INTO expression_method(expression_method_name, quantification_tool) VALUES ('%s','%s')""" % (method_expr, tool)
            try:
                self._cursor.execute(select_conditions)
                count = self._cursor.fetchone()[0]
            except mysql.connector.Error as err:
                print(Fore.RED + str(err))
            else:
                if count == 0:
                    try:
                        print(Fore.GREEN + "Trying to insert conditions infos:", info)
                        self._cursor.execute(add_conditions)
                    except mysql.connector.Error as err:
                        print(Fore.RED + str(err))
                        self._connexion.rollback()
                    else:
                        self._connexion.commit()
                else:
                    print(Fore.RED + "Duplicate entry '%s' - The insert has been ignored" % (
                    subcondition + ", " + cond_type + ", " + subcondition_type))
            try:
                self._cursor.execute(select_mthd)
                count = self._cursor.fetchone()[0]
            except mysql.connector.Error as err:
                print(Fore.RED + str(err))
                self._connexion.rollback()
            else:
                if count == 0:
                    try:
                        print(Fore.GREEN + "Trying to insert expression method : ", method_expr, tool)
                        self._cursor.execute(add_method)
                    except mysql.connector.Error as err:
                        print(Fore.RED + str(err))
                        self._connexion.rollback()
                    else:
                        self._connexion.commit()
                else:
                    print(Fore.RED + "Duplicate entry '%s' - The insert has been ignored" % (method_expr + ", " + tool))
            try:
                print(Fore.GREEN + "Trying to insert organ : ", organ)
                self._cursor.execute(add_organs)
            except mysql.connector.Error as err:
                print(Fore.RED + str(err))
                self._connexion.rollback()
            else:
                self._connexion.commit()

    def tmp_aligned_sequence(self, family: str):
        l = []
        sequence_data = self._get_data.extract_gene_and_alignment_for_family(family)
        try:
            select_gene = """SELECT idgene_family FROM gene_family WHERE gene_family_name = '%s';""" % family
            self._cursor.execute(select_gene)
            family_id = self._cursor.fetchone()[0]
        except mysql.connector.Error as err:
            print(Fore.RED + str(err))
        else:
            try:
                select_gene = """SELECT idgenes, Ensembl_ID FROM genes WHERE gene_family_idgene_family = '%s';""" % family_id
                self._cursor.execute(select_gene)
                gene_info = self._cursor.fetchall()
                for i in gene_info:
                    l.append(i[1])  # construct the list of gene ensembl ID found.
            except mysql.connector.Error as err:
                print(Fore.RED + str(err))
            else:
                if gene_info:
                    try:
                        select_gene = """SELECT idAlignment FROM Alignment WHERE gene_family_idgene_family = '%s';""" % family_id
                        self._cursor.execute(select_gene)
                        alignment_id = self._cursor.fetchone()[0]
                    except mysql.connector.Error as err:
                        print(Fore.RED + str(err))
                    else:
                        if alignment_id:
                            for gene in l:
                                for i in gene_info:
                                    try:
                                        sequence = sequence_data[gene]
                                        # check if the data already exists :
                                        select_sequence = """SELECT COUNT(*) FROM aligned_sequence WHERE sequence = '%s' and Alignment_idAlignment = '%s' and genes_idgenes = '%s';""" % (sequence, alignment_id, i[0])
                                        self._cursor.execute(select_sequence)
                                        print(self._cursor)
                                        count = self._cursor.fetchone()[0]
                                    except mysql.connector.Error as err:
                                        print(Fore.RED + str(err))
                                    else:
                                        if count == 0:
                                            try:
                                                print(Fore.GREEN + "Trying to insert sequences :", sequence)
                                                add_sequence = """INSERT INTO aligned_sequence(sequence, Alignment_idAlignment, genes_idgenes) VALUE('%s', '%s', '%s');""" % (sequence, alignment_id, i[0])
                                                self._cursor.execute(add_sequence)
                                            except mysql.connector.Error as err:
                                                print(Fore.RED + str(err))
                                                self._connexion.rollback()
                                            else:
                                                self._connexion.commit()

    def import_aligned_sequence(self, family: str):
        """
        Imports aligned sequence from the alignment file in the aligned_sequence table.

        :return: None
        """
        genes = self._get_data.extract_gene_and_alignment_for_family(family)
        for gene in genes.keys():
            sequence = genes[gene][0]
            try:
                select_gene = """SELECT COUNT(*) FROM genes WHERE Ensembl_ID = '%s';""" % gene
                self._cursor.execute(select_gene)
                count = self._cursor.fetchone()[0]
            except mysql.connector.Error as err:
                print(Fore.RED + str(err))
            else:
                if count != 0:
                    try:
                        select_idgene = """SELECT idgenes, gene_family_idgene_family FROM genes WHERE Ensembl_ID = '%s';""" % gene
                        self._cursor.execute(select_idgene)
                        ids = self._cursor.fetchall()
                        idgene = ids[0][0]
                        idfamily = ids[0][1]
                    except mysql.connector.Error as err:
                        print(Fore.RED + str(err))
                    else:
                        try:
                            select_alignment = """SELECT COUNT(*) FROM Alignment WHERE gene_family_idgene_family = '%s';""" % idfamily
                            self._cursor.execute(select_alignment)
                            count = self._cursor.fetchone()[0]
                        except mysql.connector.Error as err:
                            print(Fore.RED + str(err))
                        else:
                            if count != 0:
                                try:
                                    select_idalignment = """SELECT idAlignment FROM Alignment WHERE gene_family_idgene_family = '%s';""" % idfamily
                                    self._cursor.execute(select_idalignment)
                                    id_alignment = self._cursor.fetchone()[0]
                                except mysql.connector.Error as err:
                                    print(Fore.RED + str(err))
                                else:
                                    try:
                                        # check if the data already exists :
                                        select_sequence = """SELECT COUNT(*) FROM aligned_sequence WHERE sequence = '%s' and alignment_idalignment = '%s' and genes_idgenes = '%s';""" % (sequence, id_alignment, idgene)
                                        self._cursor.execute(select_sequence)
                                        count = self._cursor.fetchone()[0]
                                    except mysql.connector.Error as err:
                                        print(Fore.RED + str(err))
                                    else:
                                        if count == 0:
                                            try:
                                                print(Fore.GREEN + "Trying to insert sequences :", sequence)
                                                add_sequence = """INSERT INTO aligned_sequence(sequence, alignment_idalignment, genes_idgenes) VALUE('%s', '%s','%s');""" % (sequence, id_alignment,idgene)
                                                self._cursor.execute(add_sequence)
                                            except mysql.connector.Error as err:
                                                print(Fore.RED + str(err))
                                                self._connexion.rollback()
                                            else:
                                                self._connexion.commit()
                            else:
                                # print(Fore.BLUE + "No alignment found in the database for the sequence : ", sequence)
                                pass
                else:
                    # print(Fore.BLUE + "No gene found in the database for the sequence : ", sequence)
                    pass

    def import_alignments(self, family: str):
        """
        Imports the tree for the family, and the foreign key from gene_family table.

        :param family: (str) a family name
        :return: None
        """
        tree = self._get_data.extract_tree(family)
        try:
            select_nb_fam = """SELECT COUNT(*) FROM gene_family WHERE gene_family_name = '%s'""" % family
            self._cursor.execute(select_nb_fam)
            count = self._cursor.fetchone()[0]
        except mysql.connector.Error as err:
            print(Fore.RED + str(err))
        else:
            if count != 0:
                try:
                    # get family id from the gene_family table :
                    select_family = """SELECT idgene_family FROM gene_family WHERE gene_family_name = '%s'""" % family
                    self._cursor.execute(select_family)
                    id_family = self._cursor.fetchone()[0]
                except mysql.connector.Error as err:
                    print(Fore.RED + str(err))
                else:
                    try:
                        select_tree = """SELECT COUNT(*) FROM Alignment WHERE tree = '%s' and gene_family_idgene_family = '%s';""" % (
                        tree, id_family)
                        self._cursor.execute(select_tree)
                        count = self._cursor.fetchone()[0]
                    except mysql.connector.Error as err:
                        print(Fore.RED + str(err))
                    else:
                        if count == 0:
                            try:
                                # insert data into alignment table :
                                add_tree = """INSERT INTO Alignment(gene_family_idgene_family, tree) VALUES('%s', '%s')""" % (id_family, tree)
                                print(Fore.GREEN + "Trying to insert tree for family :", family)
                                self._cursor.execute(add_tree)
                            except mysql.connector.Error as err:
                                print(Fore.RED + str(err))
                                self._connexion.rollback()
                            else:
                                self._connexion.commit()
                        else:
                            print(Fore.RED + "Duplicate entry '%s, %s' - The insert has been ignored" % (id_family, tree))
            else:
                print(Fore.BLUE + "No %s found in the database : " % family)

    def import_genes(self, family: str):
        """
        Imports genes information into the database's genes table.

        :return: None
        """
        genes = self._get_data.extract_species_and_sequence_for_gene(family)
        if self._get_data.check_file_info(os.path.join(os.getcwd(), "table_equivalence.tsv")) == 0 and \
                self._get_data.check_file_info(os.path.join(os.getcwd(), "table_equivalence_mus.tsv")) == 0:
            # extract gene names :
            gene_names_dict = self._get_data.extract_gene_name(True)
        else:
            # extract gene names :
            gene_names_dict = self._get_data.extract_gene_name(False)
        for gene in genes.keys():
            species = genes[gene][1]
            try:
                # check if the family is in the database :
                select_cf = """SELECT COUNT(idgene_family) FROM gene_family WHERE gene_family_name = '%s'""" % family
                self._cursor.execute(select_cf)
                count = self._cursor.fetchone()[0]
            except mysql.connector.Error as err:
                print(Fore.RED + str(err))
            else:
                if count != 0:
                    try:
                        # select id_family of the gene :
                        select_family = """SELECT idgene_family FROM gene_family WHERE gene_family_name = '%s'""" % family
                        self._cursor.execute(select_family)
                        id_family = self._cursor.fetchone()[0]
                    except mysql.connector.Error as err:
                        print(Fore.RED + str(err))
                    else:
                        try:
                            # check if the id_species of the gene exists :
                            select_cs = """SELECT idspecies FROM species WHERE species_name = '%s'""" % species
                            self._cursor.execute(select_cs)
                            count = self._cursor.fetchone()[0]
                        except mysql.connector.Error as err:
                            print(Fore.RED + str(err))
                        else:
                            if count != 0:
                                try:
                                    # select id_species of the gene :
                                    select_species = """SELECT idspecies FROM species WHERE species_name = '%s'""" % species
                                    self._cursor.execute(select_species)
                                    id_species = self._cursor.fetchone()[0]
                                except mysql.connector.Error as err:
                                    print(Fore.RED + str(err))
                                else:
                                    try:
                                        # check for duplicate row :
                                        gene_name = gene_names_dict[gene]
                                        select_gene = """SELECT COUNT(*) FROM genes WHERE genes_name = '%s' AND Ensembl_ID = '%s' and species_idspecies = '%s' and gene_family_idgene_family = '%s';""" % (gene_name, gene, id_species, id_family)
                                        self._cursor.execute(select_gene)
                                        count = self._cursor.fetchone()[0]
                                    except mysql.connector.Error as err:
                                        print(Fore.RED + str(err))
                                    else:
                                        if count == 0:
                                            try:
                                                gene_name = gene_names_dict[gene]
                                                print(Fore.GREEN + "Trying to insert gene :", gene)
                                                add_sequence = """INSERT INTO genes(genes_name, Ensembl_ID, species_idspecies, gene_family_idgene_family) VALUES('%s' , '%s', '%s', '%s')""" % (
                                                    gene_name, gene, id_species, id_family)
                                                self._cursor.execute(add_sequence)
                                            except mysql.connector.Error as err:
                                                print(Fore.RED + str(err))
                                                self._connexion.rollback()
                                            else:
                                                self._connexion.commit()
                            else:
                                print(Fore.RED + "No species %s found in the database. Use the method import_species "
                                                 "to import %s, from your species metadata and retry." % (species, species))
                else:
                    print(Fore.RED + "No family %s found in the database. Use the method import_a_family to import %s, "
                                     "and retry." % (family, family))

    def import_expressionslevel(self, family: str):
        """
        Imports expression information from the expression file in the database's expressionlevel table.

        :return: None
        """
        expr = self._get_data.extract_expression_for_family(family=family, file=self.expression_filename)
        for i in expr:
            lenght = i[0]
            eff_lenght = i[1]
            est_counts = i[2]
            exp_level = i[3]
            try:
                print(Fore.GREEN + "Trying to insert expression level :", i)
                add_expressionlevel = """INSERT INTO expressionlevel(length, eff_count, est_count, expression_level) VALUES('%s', '%s', '%s', '%s');""" % (lenght, eff_lenght, est_counts, exp_level)
                self._cursor.execute(add_expressionlevel)
            except mysql.connector.Error as err:
                    print(Fore.RED + str(err))
                    self._connexion.rollback()
            else:
                self._connexion.commit()

    def import_genes_has_expression(self, family: str):
        """
        Imports he foreign key needed in the genes_has_expression table.

        :return: None
        """
        data = self._get_data.extract_expression_gene(self.expression_filename, family)
        for gene in data.keys():
            exp_lvl = data[gene][0]
            organ = data[gene][1][0]
            method = data[gene][1][1]
            tool = data[gene][1][2]
            condition = data[gene][1][3]
            try:
                select_cg = """SELECT COUNT(*) FROM genes WHERE Ensembl_ID = '%s'""" % gene
                self._cursor.execute(select_cg)
                count = self._cursor.fetchone()[0]
            except mysql.connector.Error as err:
                print(Fore.RED + str(err))
            else:
                if count != 0:
                    try:
                        select_gene = """SELECT idgenes FROM genes WHERE Ensembl_ID = '%s'""" % gene
                        self._cursor.execute(select_gene)
                        id_gene = self._cursor.fetchone()[0]
                    except mysql.connector.Error as err:
                        print(Fore.RED + str(err))
                    else:
                        try:
                            select_exp_lvl = """SELECT idexpressionlevel FROM expressionlevel WHERE length = '%s' AND eff_count = '%s' AND est_count = '%s' AND expression_level = '%s';""" % (
                                exp_lvl[0], exp_lvl[1], exp_lvl[2], exp_lvl[3])
                            self._cursor.execute(select_exp_lvl)
                            id_exp_lvl = self._cursor.fetchone()[0]
                        except mysql.connector.Error as err:
                            print(Fore.RED + str(err))
                        else:
                            try:
                                select_ccondition = """SELECT COUNT(*) FROM conditions WHERE subcondition = '%s' AND condition_type = '%s' AND subcondition_type = '%s'""" % (
                                    condition[0], condition[1], condition[2])
                                self._cursor.execute(select_ccondition)
                                count = self._cursor.fetchone()[0]
                            except mysql.connector.Error as err:
                                print(Fore.RED + str(err))
                            else:
                                if count != 0:
                                    try:
                                        select_ccondition = """SELECT idconditions FROM conditions WHERE subcondition = '%s' AND condition_type = '%s' AND subcondition_type = '%s'""" % (
                                            condition[0], condition[1], condition[2])
                                        self._cursor.execute(select_ccondition)
                                        id_condition = self._cursor.fetchone()[0]
                                    except mysql.connector.Error as err:
                                        print(Fore.RED + str(err))
                                    else:
                                        try:
                                            select_cexpr_mthd = """SELECT COUNT(idexpression_method) FROM expression_method WHERE quantification_tool = '%s' AND expression_method_name = '%s'""" % (
                                                tool, method)
                                            self._cursor.execute(select_cexpr_mthd)
                                            count = self._cursor.fetchone()[0]
                                        except mysql.connector.Error as err:
                                            print(Fore.RED + str(err))
                                        else:
                                            if count != 0:
                                                try:
                                                    select_expr_mthd = """SELECT idexpression_method FROM expression_method WHERE quantification_tool = '%s' AND expression_method_name = '%s'""" % (
                                                        tool, method)
                                                    self._cursor.execute(select_expr_mthd)
                                                    id_exp_mthd = self._cursor.fetchone()[0]
                                                except mysql.connector.Error as err:
                                                    print(Fore.RED + str(err))
                                                else:
                                                    try:
                                                        select_corgan = """SELECT COUNT(idorgans) FROM organs WHERE organ_name = '%s'""" % organ
                                                        self._cursor.execute(select_corgan)
                                                        count = self._cursor.fetchone()[0]
                                                    except mysql.connector.Error as err:
                                                        print(Fore.RED + str(err))
                                                    else:
                                                        if count != 0:
                                                            try:
                                                                select_organ = """SELECT idorgans FROM organs WHERE organ_name = '%s'""" % organ
                                                                self._cursor.execute(select_organ)
                                                                id_organ = self._cursor.fetchone()[0]
                                                            except mysql.connector.Error as err:
                                                                print(Fore.RED + str(err))
                                                            else:
                                                                try:
                                                                    select_gene_has_exp = """SELECT COUNT(*) FROM gene_has_expression WHERE genes_idgenes = '%s' and expressionlevel_idexpressionlevel = '%s' and expression_method_idexpression_method = '%s' and conditions_idconditions = '%s' and organs_idorgans = '%s';""" % (
                                                                        id_gene, id_exp_lvl, id_exp_mthd, id_condition,
                                                                        id_organ)
                                                                    self._cursor.execute(select_gene_has_exp)
                                                                    count = self._cursor.fetchone()[0]
                                                                except mysql.connector.Error as err:
                                                                    print(Fore.RED + str(err))
                                                                    self._connexion.rollback()
                                                                else:
                                                                    if count ==0:
                                                                        try:
                                                                            print(Fore.GREEN + "Trying to insert genes_has_expression :")
                                                                            add_gene_has_exp = """INSERT INTO gene_has_expression(genes_idgenes, expressionlevel_idexpressionlevel, expression_method_idexpression_method, conditions_idconditions, organs_idorgans) VALUES('%s', '%s', '%s', '%s', '%s')""" % (
                                                                            id_gene, id_exp_lvl, id_exp_mthd, id_condition,
                                                                            id_organ)
                                                                            self._cursor.execute(add_gene_has_exp)
                                                                        except mysql.connector.Error as err:
                                                                            print(Fore.RED + str(err))
                                                                            self._connexion.rollback()
                                                                        else:
                                                                            self._connexion.commit()

    def close_database(self):
        """
        Close the connexion to the database.

        :return: close_cnx (str): The
        """
        close_cnx = Fore.GREEN + "The connexion is closed"
        self._cursor.close()
        self._connexion.close()
        return close_cnx


def main():
    importdata = ImportData(path_directory, database_configuration, exp_filename)
    importdata.import_a_family('F00002')
    importdata.import_species(species_metadata_file)
    importdata.import_organs_expression_method_condition()
    importdata.import_expressionslevel('F00002')
    importdata.import_alignments('F00002')
    importdata.import_genes('F00002')
    importdata.import_aligned_sequence('F00002')
    importdata.import_genes_has_expression('F00002')
    importdata.close_database()

main()
