import argparse  # command-line parsing module

# Get argument and parse them
# TODO : ajouter explication dans le README
parser = argparse.ArgumentParser()
# directory path :
parser.add_argument("-d", "--directory", help='Path to data directory', required=True)
# expression level file :
parser.add_argument("-e", "--expression", help='Expression level exp_filename', required=True)
# species_metadata_file metadata file :
parser.add_argument("-s", "--species", help='Species metadata exp_filename', required=True)
# family name :
parser.add_argument("-f", "--family", help='Gene family name', required=False)
args = parser.parse_args()
