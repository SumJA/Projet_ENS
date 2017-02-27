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
    """
    A data extractor:
        Extract data from a file containing all :
            - the alignments information
            - phylogenetic trees
            - level of expression
            - information on the species analyzed

    :Attributes: path_directory : (str) The data directory path.
                data : (dict) A dictionary with all the extracted information. The keys are the genes families.
    """
    def __init__(self, path: str):
        """
        :param path: (str) Path to the data directory.
        """
        # Get OS info :
        if platform.uname().system == "Windows":
            self.__sign = "\\"
        else:
            self.__sign = "/"
        if self.check_path_info(path) == 0:
            self.path_directory = path
            self._alignments_path = self._get_all_directories_path()[0]
            self._expression_level_path = self._get_all_directories_path()[1]
            self._tree_path = self._get_all_directories_path()[2]
            self._seq2sp_path = self._get_all_directories_path()[3]
        self.data = {}

    @staticmethod
    def check_path_info(path: str):
        """
        Check if a given path exists.

        :param path: (str) Path to a directory.
        :return: 0 if all went well - Else print an exception.
        """
        try:
            assert os.path.isdir(path)
            return 0
        except AssertionError as Ae:
            print(Ae)
            print(Fore.RED + "ERROR : Unable to find the directory : "
                             "the directory does not exist OR no read permissions")

    @staticmethod
    def check_file_info(file: str):
        """
        Check if a given file exists.

        :param file: (str) Path to a file.
        :return: 0 if all went well - Else print an exception.
        """
        try:
            assert os.path.exists(file)
            return 0
        except AssertionError as Ae:
            print(Ae)
            print(Fore.RED + "ERROR : Unable to open file : the file does not exist OR no read permissions")

    def _get_all_directories_path(self):
        """
        Find path to :
            - alignments directory called "Alignments"
            - expression_levels directory called "ExpressionLevels"
            - Gene trees directory called "GeneTrees"
            - Seq2Sp directory called "Seq2SpTab"

        If the directories cannot be found the function print an exception.

        :return: alignments, expression_levels, tree, seq2sp
            the function return the path to the directories in a list:
                - first element : path to Alignments (str)
                - second element : path to ExpressionLevels (str)
                - third element : path to GeneTrees (str)
                - forth element : path to Seq2SpTab (str)
        """
        # FIXME : utilser os.path.join
        # TODO : possibilité d'utiliser des chemins fourni lors du parsage ?
        alignments = self.path_directory + self.__sign + "Alignments"
        self.check_path_info(alignments)  # Check if the Alignments directory exists
        expression_levels = self.path_directory + self.__sign + "ExpressionLevels"
        self.check_path_info(expression_levels)  # Check if the ExpressionLevels directory exists
        tree = self.path_directory + self.__sign + "GeneTrees"
        self.check_path_info(tree)  # Check if the GeneTrees directory exists
        seq2sp = self.path_directory + self.__sign + "Seq2SpTab"
        self.check_path_info(seq2sp)  # Check if the Seq2SpTab directory exists
        return alignments, expression_levels, tree, seq2sp

    @staticmethod
    def _extract_families_names(directory: str):
        """
        Extracts gene families names from fasta files and files ending with "_Seq2Sp.tsv" in a specified directory.

        :param directory: (str) Path to a directory.
        :return: l a list of str with all the family names.
        """
        l = []
        files = os.listdir(directory)  # list of all the files in the directory.
        for file in files:
            if "fasta" in file:
                l.append(file[:-6])
            elif "_Seq2Sp.tsv" in file:
                l.append(file[:-11])
        return l

    def extract_all_families(self):
        """
        Initialise a dictionary with all the families found in the alignment directory.
        The keys are the families name and they have None value.
        The families names are extracted from the fasta file name or the files ending with "_Seq2Sp.tsv".

        :return: f (dict): a dictionary initialised with all the families found as a key and with None value.
        """
        f = {}
        family = self._extract_families_names(self._alignments_path)  # Extract families name
        for i in family:
            f[i] = None
        return f

    def extract_all_species(self, filename: str):
        """
        Initialise a list with all the species and their relative data found in the given file.

        :param filename: (str) a .tsv file with the species metadata
        :return: l a list of str with all the species information.
                    You first have the Species_name, then the Species_Taxid, the Assembly_name, the Assembly_source
                    and finally the Species_Classification.
                    For exemple : ["Mustela_putorius_furo", "9669", "MusPutFur1.0", "Ensembl",
                    "Mustelinae-Mustelidae-Caniformia-Carnivora-Laurasiatheria-Eutheria-Mammalia-Euteleostomi-Vertebrata-Craniata-Chordata-Metazoa-Eukaryota",
                    "Callithrix_jacchus",	"9483", "C_jacchus3.2.1",	"Ensembl",
                    "Callitrichinae-Cebidae-Platyrrhini-Haplorrhini-Primates-Euarchontoglires-Eutheria-Mammalia-Euteleostomi-Vertebrata-Craniata-Chordata-Metazoa-Eukaryota"]
        """
        l = []
        # FIXME : utilser os.path.join
        # TODO : faire une liste de liste
        file = self.path_directory + self.__sign + filename
        self.check_file_info(file)  # check if the file exists
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

    def extract_gene_and_alignment_for_family(self, family_name: str):
        """
        Extracts genes and its aligned sequence for the family from its alignment file.

        :param family_name: (str) A family name.
        :return: gene_name: (dict) A dictionary of all the genes with their aligned sequence for the given family.
                    The keys are the gene ID and the values are the sequences.
        """
        gene_name = {}
        # FIXME: utilser os.path.join
        file = self._alignments_path + self.__sign + family_name + ".fasta"
        self.check_file_info(file)  # check if the file exists
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

    def extract_tree(self, family_name: str):
        """
        Extracts trees for the family from its Newick (.tree) file in the GeneTree directory.

        :param family_name: (str) A family name.
        :return: tree (list) a list of trees for the given family.
        """
        tree = []
        # FIXME: utilser os.path.join
        file = self._tree_path + self.__sign + family_name + ".tree"
        self.check_file_info(file)  # check if the file exists
        try:
            f = open(file, "r")
            for line in f:
                tree = line
            f.close()
            return tree
        except OSError:
            print(Fore.RED + "ERROR : Failed to open _tree_path file : ", file)

    def extract_species_and_sequence_for_gene(self, family_name: str):
        """
        Extracts the species names for the genes of a family and their aligned sequence.

        :param family_name: (str) A family name.
        :return: genes: (dict) a dictionary with all the genes of the family, their aligned sequence and their species.
                    the keys are the genes and their values are the species name and their aligned sequence.
        """
        # FIXME: utilser os.path.join
        file = self._seq2sp_path + self.__sign + family_name + "_Seq2Sp.tsv"
        self.check_file_info(file)  # check if the file exists
        genes = self.extract_gene_and_alignment_for_family(family_name)  # genes dictionary with their aligned sequence.
        try:
            with open(file, 'r') as tsv:
                for line in csv.reader(tsv, delimiter="\t"):
                    gene = line[0][:-7]
                    species = line[1]
                    genes[gene].append(species)
            return genes
        except OSError:
            print(Fore.RED + "ERROR : Failed to open alignment file : ", file)

    def extract_expression_info(self, file: str):
        """
        Extracts expression information and their condition from the file.

        :param file: (str) a expression levels file.
        :return: organ (str), method (str), tool (str), l_condition (list of str)
                the function return a list with the organ, then the method use to get the expression level, the tool use
                and all a list of condition.

                the list of condition contain the subcondition information, the condition and the subcondition type.
        """
        organ = None
        method = None
        tool = None
        l_condition = []
        self.check_file_info(file)  # check if the file exists
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

    def extract_expression_and_all_information_for_family(self, file: str, family: str):
        """
        Extracts all the information for a family and update the data dictionary with it.

        :param file: (str) a expression_level file.
        :param family: (str) a family name.
        :return: exp a list of list with all the expression information (length, eff_kength, est_counts, exp_level) for
                every gene of the family.
        """
        done_family = []
        i = 0
        exp = []
        # FIXME: utilser os.path.join
        filename = self._expression_level_path + self.__sign + file
        self.check_file_info(filename)  # check if the file exists
        try:
            with open(filename, 'r') as tsv:
                for line in csv.reader(tsv, delimiter="\t"):
                    if i != 0:
                        gene = line[0][:-7]
                        while family == line[0][-6:]:
                            length = line[1]
                            eff_length = line[2]
                            est_counts = line[3]
                            exp_level = line[4]
                            l = [length, eff_length, est_counts, exp_level]
                            exp.append(l)
                            # extract gene information with their species and their aligned sequence:
                            genes = self.extract_species_and_sequence_for_gene(family)
                            genes[gene].append(l)
                            if family not in done_family:
                                # extract tree for the family
                                tree = self.extract_tree(family)
                                self.data[family] = [tree, genes]
                            break
                    i += 1
            return exp
        except OSError:
            print(Fore.RED + "ERROR : Failed to open expression file : ", file)

    def get_data_for_expression_file(self, file: str, family: str):
        """
        Get all the data available for a family.

        :param file: (str) Path to expression level file.
        :param family: (str) A family name.
        :return: data (dict) a dictionary with all the data of the family.
                    The key is the family name and its value is a list with its gene tree and an another dictionary.
                    This other dictionary contains all the information of the family genes : the key is the gene EMBL ID
                    and its values are :
                        - eligned sequence
                        - species
                        - expression levels
        """
        self.extract_expression_and_all_information_for_family(file, family)
        return self.data


# TODO : replace with parse argument :
# path to the directory with data to import :
path_directory = "C:\\Users\sumja_000\Documents\COURS\Projet2\données\ProjetM1BioInfo\Version1"
