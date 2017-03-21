import sys, requests
from pprint import pprint
import json


def idEnsembl_to_nomGene(EnsemblID):
    server = "http://rest.ensembl.org"
    ext = "/xrefs/id/" + EnsemblID + "?"

    r = requests.get(server + ext, headers={"Content-Type": "application/json"})

    if not r.ok:
        r.raise_for_status()
        sys.exit()

    json_file = r.json()
    ensembl_name = json_file[1]["display_id"]
    print(ensembl_name)


idEnsembl_to_nomGene("ENSG00000139618")
