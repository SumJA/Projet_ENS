##Test2 Olivier
import platform
import os
from colorama import Fore  # color console module
import argparse  # command-line parsing module

# Get argument and parse them
# TODO : tuto => https://docs.python.org/3/howto/argparse.html :
# il faut donner des paramètres pour localiser le dossier avec les données
# TODO : ajouter explication dans le README
parser = argparse.ArgumentParser()
parser.parse_args()


class GetData:
    # TODO : documentation : see example of documentation at http://thomas-cokelaer.info/tutorials/sphinx/docstring_python.html
    def __init__(self, path):
        # Get OS info :
        if platform.uname().system == "Windows":
            self._sign = "\\"
        else:
            self._sign = "/"
        if self.check_path_info(path) == 0:
            self.path_directory = path  # The directory path
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
            assert os.path.exists(path)
            return 0
        except AssertionError as Ae:
            print(Ae)
            print(Fore.RED + "ERROR : Unable to open file : the file does not exist OR no read permissions")

    def get_all_directories_path(self):
        # TODO : documentation
        """
        :return: alignments, expression_levels, tree, seq2sp
        """
        alignments = self.path_directory + self._sign + "Alignments"
        self.check_path_info(alignments)
        expression_levels = self.path_directory + self._sign + "ExpressionLevels"
        self.check_path_info(expression_levels)
        tree = self.path_directory + self._sign + "GeneTrees"
        self.check_path_info(tree)
        seq2sp = self.path_directory + self._sign + "Seq2SpTab"
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

    def _init_data(self):
        # TODO : documentation
        """
        Initialize self.data a dictionary of data with all the family names
        :return: 0 if all went well
        """
        alignments = self.get_all_directories_path()[0]  # TODO : pour le moment on ne prend en compte que les noms de familles dans le dossier Alignments. Essayé de le faire toutes les dossiers
        family = self._extract_families_names(alignments)
        for i in family:
            self.data[i] = []

    def init_gene_from_alignments_for_family(self, family_name): # TODO : faire en sorte que ça marche auto pour chaque famille. Ce sera fait à l'aide d'une nouvelle fonction éventuellement.
        # TODO : documentation
        """
        :param family_name: str => a family name
        :return: gene_dict: dict => a dictionary of all the genes for the given family
        """
        gene_name = []
        self._init_data()  # initialize data dictionary with all the families name
        alignments = self.get_all_directories_path()[0]
        file = alignments + self._sign + family_name + ".fasta"
        f = open(file, "r")
        for line in f.readlines():  # TODO : gestion erreurs
            if line[0] == ">":
                gene_name.append(line[1:line.find("_")])
            self.data[family_name] = gene_name
            f.close()
        return 0

    # TODO : faire le lien entre un gène et une espèce => faire en sorte que dans self.data : famille est une clé de gène,
    # TODO : suite : gène est une clé d'espèce, d'expression et d'alignement. L'alignement est une clé d'arbre.
    # TODO: suite : expressio est une clé de condition, d'organe et de méthode d'expression.

    def get_organ(self, file):
        # TODO : documentation
        organ = None
        f = open(file, "r")
        for line in f.readlines():
            if line[:19] == "RNA_seq_condition: ":
                organ = line[19:]
        f.close()
        return organ

    def get_tree(self, family_name):
        # TODO : documentation
        gene_dict = {}
        tree = []
        genetree = self.get_all_directories_path()[2]
        file = genetree + self._sign + family_name + ".tree"
        f = open(file, "r")
        for line in f:
            tree = line
        f.close()
        return tree


# TODO : replace with parse argument :
# path to the directory with data to import :
path_directory = "C:\\Users\sumja_000\Documents\COURS\Projet2\données\ProjetM1BioInfo\Version1"
# Tests :
data = GetData(path_directory)
data.get_all_directories_path()
data.init_gene_from_alignments_for_family("F00000")
print(data.data)
