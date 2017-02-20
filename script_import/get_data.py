import platform
import os
from colorama import Fore  # color console module
import argparse  # command-line parsing module
import re

# Get argument and parse them
# TODO : tuto => https://docs.python.org/3/howto/argparse.html
parser = argparse.ArgumentParser()
parser.parse_args()


class Data:
    def __init__(self, path):
        # Get OS info :
        # TODO : à utiliser pour savoir comment se déplacer dans l'arborescence de fichiers
        self.os_info = platform.uname().system
        if self.check_path_info(path) == 0:
            self.path_directory = path
            self.get_gene()

    @staticmethod
    def check_path_info(path):
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

    def get_all_directory(self):
        """
        Get path to the all data directory
        :return: alignments path, expression_levels path, tree path, seq2Sp path
        """
        # TODO : make it work for linux !
        self.check_path_info(self.path_directory)
        alignments = self.path_directory + "\\Alignments"
        expression_levels = self.path_directory + "\\ExpressionLevels"
        tree = self.path_directory + "\\GeneTrees"
        seq2Sp = self.path_directory + "\\Seq2SpTab"
        self.check_path_info(alignments)
        self.check_path_info(expression_levels)
        self.check_path_info(tree)
        self.check_path_info(seq2Sp)
        return alignments, expression_levels, tree, seq2Sp

    def get_family(self):
        """
        Get family names
        :return: liste a list with all the family names
        """
        liste = []
        alignments = self.get_all_directory()[0]
        files = os.listdir(alignments)
        for file in files:
            if "fasta" in file:
                liste.append(file[:-6])
        return liste

    def get_gene(self, family_name):
        """
        Get gene names for a given family
        :param family_name: str => a family name
        :return: gene_dict: dict => a dictionary of all the genes for the given family
        """
        gene_dict = {}
        gene_name = []
        alignments = self.get_all_directory()[0]
        file = alignments + "\\" + family_name + ".fasta"
        f = open(file, "r")
        for line in f.readlines():
            if line[0] == ">":
                gene_name.append(line[1:line.find("_")])
            gene_dict[family_name] = gene_name
            f.close()
        return gene_dict



# TODO : replace with parse argument :
# path to the directory with data to import :
path_directory = "C:\\Users\sumja_000\Documents\COURS\Projet2\données\ProjetM1BioInfo\Version1"

data = Data(path_directory)
data.get_all_directory()
data.get_family()
print(data.get_gene("F00000"))

# Check if the given path exists :
# check_path_info(path_directory)
