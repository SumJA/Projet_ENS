import platform
import os
from colorama import Fore  # color console module
import argparse  # command-line parsing module
import csv  # csv / tsv reader module

# Get argument and parse them
# TODO : tuto => https://docs.python.org/3/howto/argparse.html :
# il faut donner des paramètres pour localiser le dossier avec les données
# TODO : ajouter explication dans le README
parser = argparse.ArgumentParser()
parser.parse_args()


class GetData:
    # FIXME : VERY IMPORTANT !!!!!! : fuite mémoire car ouverture des fichiers en cascade !! Oui j'ai codé comme de la merde :'( Se limiter à 68 familles pour le moment
    # TODO : documentation : see example of documentation at
    # http://thomas-cokelaer.info/tutorials/sphinx/docstring_python.html
    def __init__(self, path):
        # Get OS info :
        if platform.uname().system == "Windows":
            self.__sign = "\\"
        else:
            self.__sign = "/"
        if self.check_path_info(path) == 0:
            self.path_directory = path  # The directory path
            self._alignments_path = self._get_all_directories_path()[0]
            self._expression_level_path = self._get_all_directories_path()[1]
            self._tree_path = self._get_all_directories_path()[2]
            self._seq2sp_path = self._get_all_directories_path()[3]
        self.data = {}  # Dictionnaire qui devra conternir toutes les données : ce sera un dictionnaire
                        # Avec en clé les noms de familles

    @staticmethod
    def check_path_info(path):
        # TODO : documentation
        """
        Check if a given path exists
        :param path: str
        :return: 0 OR print an exception
        """
        try:
            assert os.path.isdir(path)
            return 0
        except AssertionError as Ae:
            print(Ae)
            print(Fore.RED + "ERROR : Unable to find the directory : "
                             "the directory does not exist OR no read permissions")

    @staticmethod
    def check_file_info(file):
        # TODO : documentation
        """
        Check if a given path exists
        :param path: str
        :return: 0 OR print an exception
        """
        try:
            assert os.path.exists(file)
            return 0
        except AssertionError as Ae:
            print(Ae)
            print(Fore.RED + "ERROR : Unable to open file : the file does not exist OR no read permissions")

    def _get_all_directories_path(self):
        # TODO : documentation
        """
        :return: _alignments_path, expression_levels, _tree_path, _seq2sp_path
        """
        alignments = self.path_directory + self.__sign + "Alignments"
        self.check_path_info(alignments)
        expression_levels = self.path_directory + self.__sign + "ExpressionLevels"
        self.check_path_info(expression_levels)
        tree = self.path_directory + self.__sign + "GeneTrees"
        self.check_path_info(tree)
        seq2sp = self.path_directory + self.__sign + "Seq2SpTab"
        self.check_path_info(seq2sp)
        return alignments, expression_levels, tree, seq2sp

    @staticmethod
    def _extract_families_names(directory):
        # TODO : documentation
        """
        Extract families names from filename in a specified directory
        :return: l a list with all the family names
        """
        l = []
        files = os.listdir(directory)
        for file in files:
            if "fasta" in file:
                l.append(file[:-6])
            elif "_Seq2Sp.tsv" in file:
                l.append(file[:-11])
        return l

    def extract_all_families(self):
        # TODO : documentation
        """
        Initialize self.data a dictionary of data with all the family names
        :return: 0 if all went well
        """
        family = self._extract_families_names(self._alignments_path)
        for i in family:
            self.data[i] = None

    def extract_all_species(self, filename):
        # TODO : documentation
        l = []
        file = self.path_directory + "\\" + filename
        if self.check_file_info(file) == 0:
            try:
                i = 0
                with open(file, 'r') as tsv:
                    for line in csv.reader(tsv, delimiter="\t"):
                        if i == 0:
                            pass
                        else:
                            l.append(line)
                        i += 1
                return l
            except OSError:
                print(Fore.RED + "ERROR : Failed to open species metadata file : ", filename)

    def extract_gene_and_alignment_for_family(self, family_name):
        # TODO : documentation
        """
        :param family_name: str => a family name
        :return: gene_name: dict => a dictionary of all the genes with their aligned sequence for the given family
        """
        gene_name = {}
        file = self._alignments_path + self.__sign + family_name + ".fasta"
        try:
            f = open(file, "r")
            for line in f:
                if line[0] == ">":
                    gene = line[1:line.find("_")]
                    line = next(f)
                    seq = line.splitlines()
                    gene_name[gene] = seq
            f.close()
            return gene_name
        except OSError:
            print(Fore.RED + "ERROR : Failed to open alignment file : ", file)

    def extract_tree(self, family_name):
        # TODO : documentation
        tree = []
        file = self._tree_path + self.__sign + family_name + ".tree"
        try:
            f = open(file, "r")
            for line in f:
                tree = line
            f.close()
            return tree
        except OSError:
            print(Fore.RED + "ERROR : Failed to open _tree_path file : ", file)

    def extract_species_for_gene(self, family_name):
        # TODO : documentation
        file = self._seq2sp_path + self.__sign + family_name + "_Seq2Sp.tsv"
        genes = self.extract_gene_and_alignment_for_family(family_name)
        try:
            f = open(file, "r")
            with open(file, 'r') as tsv:
                for line in csv.reader(tsv, delimiter="\t"):
                    gene = line[0][:-7]
                    species = line[1]
                    genes[gene].append(species)
            return genes
        except OSError:
            print(Fore.RED + "ERROR : Failed to open alignment file : ", file)

    def extract_expression_info(self, file):
        # TODO : documentation
        organ = None
        method = None
        tool = None
        l_condition = []
        if self.check_file_info(file) == 0:
            try:
                f = open(file, "r")
                for line in f.readlines():
                    if line[:19] == "RNA_seq_condition: ":
                        organ = line[19:]
                    elif line[:23] == "Quantification_method: ":
                        method = line[23:]
                    elif line[:21] == "Quantification_tool: ":
                        tool = line[21:]
                    elif line[:22] == "RNA_seq_subcondition: ":
                        l_condition.append(line[22:])
                    elif line[:24] == "RNA_seq_condition_type: ":
                        l_condition.append(line[24:])
                    elif line[:27] == "RNA_seq_subcondition_type: ":
                        l_condition.append(line[27:])
                f.close()
                return organ, method, tool, l_condition
            except OSError:
                print(Fore.RED + "ERROR : Failed to open expression metadata file : ", file)
        else:
            print(Fore.RED + " ERROR : Can't find expression metadata file : ", file)

    def extract_expression_levels(self, file):
        # TODO : documentation
        done_family = []
        i = 0
        exp = []
        filename = self._expression_level_path + self.__sign + file
        if self.check_file_info(filename) == 0:
            try:
                with open(filename, 'r') as tsv:
                    for line in csv.reader(tsv, delimiter="\t"):
                        if i != 0:
                            gene = line[0][:-7]
                            family = line[0][-6:]
                            f = family
                            length = line[1]
                            eff_length = line[2]
                            est_counts = line[3]
                            exp_level = line[4]
                            l = [length, eff_length, est_counts, exp_level]
                            exp.append(l)
                            genes = self.extract_species_for_gene(family)
                            genes[gene].append(l)
                            if family not in done_family:
                                tree = self.extract_tree(family)
                                self.data[family] = [tree, genes]
                        i += 1
                return exp
            except OSError:
                print(Fore.RED + "ERROR : Failed to open expression file : ", file)
        else:
            print(Fore.RED + " ERROR : Can't find expression file : ", file)

    def get_data_for_expression_file(self, file):
        # TODO :documentation
        self.extract_expression_levels(file)
        return self.data


class ImportData(GetData):
    # TODO : documentation
    def __init__(self, path):
        GetData.__init__(self, path)


# TODO : replace with parse argument :
# path to the directory with data to import :
path_directory = "C:\\Users\sumja_000\Documents\COURS\Projet2\données\ProjetM1BioInfo\Version1"

# Tests :
data = GetData(path_directory)
data.get_data_for_expression_file("Mus_musculus.KidneyControle.quant.tsv")
print(data.data)