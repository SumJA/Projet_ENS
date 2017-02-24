import mysql.connector
#import get_data


class ImportData():
    # TODO : documentation
    def __init__(self, path):
        self.getdata = GetData(path)
        self.all_data = {}
        self.cnx = mysql.connector.connect(user='', password='', host='', database='')
        self.cursor = self.cnx.cursor()

    def import_families(self, file):
        families = self.getdata.extract_all_families()
        i = 0
        for family in families:
            print(i)
            i = i + 1
            self.all_data = self.getdata.get_data_for_expression_file(file, family)


    family_name = dictionnaire[0]
    nom_gene =
    id_gene =
    alignment =
    tree =
    expression =
    species =
    organ =
    expression_method =
    condition =

    try:
        for fg in family_gene:
            if family_gene[fg] =! family_gene[fg-1]:
                cursor.execute("""INSERT INTO gene_family(gene_family_name) VALUES(?)""", (family_gene))


        for g in id_gene:
            cursor.execute("""INSERT INTO genes(Ensembl_ID) VALUES(?)""", (id_gene))

        for a in alignment:
            cursor.execute("""INSERT INTO alignment(alignment_data) VALUES(?)""", (alignment))

        for t in tree:
            cursor.execute("""INSERT INTO tree(tree_data) VALUES(?)""", (tree))

        for e in expression:
            length = expression[0] #supposition de ma part
            eff_count = expression[1]
            est_count = expression[2]
            expression_level = expression[3]
            cursor.execute("""INSERT INTO expression(length, eff_count, est_count, expression_level) VALUES(?, ?, ?, ?)""", (length, eff_count, est_count, expression_level))

        for s in species:
            cursor.execute("""INSERT INTO species(species_name) VALUES(?)""", (species))

        for o in organ:
            cursor.execute("""INSERT INTO organs(organ_name) VALUES(?)""", (organ))

        for em in expression_method:
            cursor.execute("""INSERT INTO expression_method(expression_method_name) VALUES(?)""", (expression_method))

        for c in condition:
            dvp_stage = condition[0]
            state = condition[1]
            #je ne vois pas rop ce que c'est ces deux trucs mdr
            cursor.execute("""INSERT INTO conditions(dvp_stage, state) VALUES(?, ?)""", (dvp_stage, state))


    # Make sure data is committed to the database
    cnx.commit()

    except sqlite3.OperationalError as b:
        print(b)
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()


    cursor.close()
    cnx.close()


# TODO : replace with parse argument :
# path to the directory with data to import :
path_directory = "C:\\Users\sumja_000\Documents\COURS\Projet2\données\ProjetM1BioInfo\Version1"

# Tests :
data = GetData(path_directory)
import_data = ImportData(path_directory)
import_data.import_families("Mus_musculus.KidneyRestriction.quant.tsv")