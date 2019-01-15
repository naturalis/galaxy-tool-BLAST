"""

"""
from Bio import SeqIO

def make_taxon_dict():
    taxonDict = {}
    with open("taxmap_slv_ssu_ref_132.txt") as silvaTaxonomy:
        for x in silvaTaxonomy:
            x = x.strip().split("\t")
            accession = x[0]
            taxonomy = x[3]
            species = x[-2]
            if accession not in taxonDict:
                taxonDict[accession] = taxonomy+species
    print "dictmade"
    return taxonDict

def add_taxonomy(taxonDict):
    with open("SILVA_132_SSURef_tax_silva.fasta", "r") as silva, open("SILVA_132_SSURef_tax_silva_taxonomy.fasta", "a") as output:
        for record in SeqIO.parse(silva, "fasta"):
            accession = str(record.id).split(".")[0]
            #print accession
            newHeader = ">silva|"+str(record.id)+"|"+taxonDict[accession]+"\n"
            output.write(newHeader+str(record.seq)+"\n")

def main():
    taxonDict = make_taxon_dict()
    add_taxonomy(taxonDict)

if __name__ == "__main__":
    main()
