import mysql.connector, os
from script_import import get_data
import requests, sys

path_directory = "/media/elisa/Windows/Users/UTILISATEUR/Documents/M1/S2/Projets/ProjetM1BioInfo.tar/ProjetM1BioInfo/ProjetM1BioInfo/Version1"

class ImportData():
    # TODO : documentation
    def __init__(self, path):
        self.getdata = get_data.GetData(path)
        self.cnx = mysql.connector.connect(user='elisa', password='*elisa*1995', host='127.0.0.1', database='projetENS')
        self.cursor = self.cnx.cursor()

    def import_families(self):
        for fg in list(set(self.getdata._extract_families_names(self.getdata._alignments_path))):
            add_family_name = ("INSERT INTO gene_family" "(gene_family_name)" "VALUES(%s);")
            data_family_name = (fg,)
            self.cursor.execute(add_family_name, data_family_name)

    def import_genes(self):  # marche pas encore car faut récupérer nom des gènes
        for family in list(set(self.getdata._extract_families_names(self.getdata._alignments_path))):
            for key in self.getdata.extract_gene_and_alignment_for_family(family).keys():
                gene_name = self.ensemblID_to_geneName(key)
                add_gene_name_and_EnsemblID = ("INSERT INTO genes" "(Ensembl_ID)" "VALUES(%s);")
                data_gene_name_and_EnsemblID = (key,)
                self.cursor.execute(add_gene_name_and_EnsemblID, data_gene_name_and_EnsemblID)

    def ensemblID_to_geneName(self, ensemblID):

        server = "http://rest.ensembl.org"
        ext = "/archive/id/" + ensemblID + "?"

        r = requests.get(server + ext, headers={"Content-Type": "application/json"})

        if not r.ok:
            r.raise_for_status()
            sys.exit()

        decoded = r.json()
        print(repr(decoded))
        return 0

    def import_alignments(
            self):  # marche pas car dans base de données c'est "VARCHAR 45" sauf que les alignments sont plus longs et que je n'arrive pas à y changer dans la bdd
        for family in list(set(self.getdata._extract_families_names(self.getdata._alignments_path))):
            for value in self.getdata.extract_gene_and_alignment_for_family(family).values():
                add_alignments = ("INSERT INTO alignment" "(alignment_data)" "VALUES(%s);")
                data_alignments = (value,)
                self.cursor.execute(add_alignments, data_alignments)

    def import_tree(
            self):  # marche pas car dans base de données c'est "VARCHAR 45" sauf que les alignments sont plus longs et que je n'arrive pas à y changer dans la bdd
        for family in list(set(self.getdata._extract_families_names(self.getdata._alignments_path))):
            for tree in self.getdata.extract_tree(family):
                add_tree = ("INSERT INTO tree" "(tree_data)" "VALUES(%s);")
                data_tree = (tree,)
                self.cursor.execute(add_tree, data_tree)

    def import_expressions(self):  # marche pas encore car faut remplir les clés étrangères
        for family in list(set(self.getdata._extract_families_names(self.getdata._alignments_path))):
            directory = os.listdir(self.getdata._expression_level_path)
            for element in directory:
                if not os.path.isdir(element):
                    if element.endswith("quant.tsv"):
                        exps = self.getdata.extract_expression_levels(element, family)
                        for exp in exps:
                            length = exp[0]
                            eff_length = exp[1]
                            est_counts = exp[2]
                            exp_level = exp[3]
                            add_expression_data = (
                            "INSERT INTO expression" "(length, eff_count, est_count, expression_level)" "VALUES(%s,%s,%s,%s)")
                            data_expression_data = (length, eff_length, est_counts, exp_level,)
                            self.cursor.execute(add_expression_data, data_expression_data)

    def import_species(self):  # marche pas car duplication --> à gérer
        for family in list(set(self.getdata._extract_families_names(self.getdata._alignments_path))):
            for specie in self.getdata.extract_species_for_gene(family).values():
                add_species = ("INSERT INTO species" "(species_namel)" "VALUES(%s);")  # erreur de frappe sur "namel" ^^
                data_species = (specie[1],)
                self.cursor.execute(add_species, data_species)

    def import_organs_expressionMethod_condition(
            self):  # marche pas encore car pour "state" ça récupère une liste : par exemple :  ['Control\n', 'Discret\n', 'Discret \n'] et du coup on prend lequel là dedans ?? mais on peut pas rentrer une liste dans la base de données
        directory = os.listdir(self.getdata._expression_level_path)
        for element in directory:
            if not os.path.isdir(element):
                if element.endswith("metadata.tsv"):
                    exps_info = self.getdata.extract_expression_info(
                        self.getdata._expression_level_path + "/" + element)
                    add_organ = ("INSERT INTO organs" "(organ_name)" "VALUES(%s);")
                    data_organ = (exps_info[0],)
                    self.cursor.execute(add_organ, data_organ)
                    add_expression_method = ("INSERT INTO expression_method" "(expression_method_name)" "VALUES(%s);")
                    data_expression_method = (exps_info[1],)
                    self.cursor.execute(add_expression_method, data_expression_method)
                    add_condition = ("INSERT INTO conditions" "(dvp_stage, state)" "VALUES(%s, %s);")
                    data_condition = (exps_info[2], exps_info[3],)
                    self.cursor.execute(add_condition, data_condition)

    def close_database(self):
        self.cnx.commit()
        self.cursor.close()
        self.cnx.close()


def main():
    print("test")
    importdata = ImportData(path_directory)
    getdata = get_data.GetData(path_directory)
    #    importdata.import_families()
    importdata.import_genes()
    #    importdata.import_alignments()
    #    importdata.import_tree()
    #    importdata.import_expressions()
    #    importdata.import_species()
    # importdata.import_organs_expressionMethod_condition()
    importdata.close_database()

main()
