"""

"""
from Bio import SeqIO

# Retrieve the commandline arguments
parser = argparse.ArgumentParser(description='Add taxonomy to silva')
parser.add_argument('-f', dest='fasta', type=str, required=True)
parser.add_argument('-t', dest='taxonomy', type=str, required=True)
parser.add_argument('-o', dest='output', type=str, required=True)
args = parser.parse_args()

def make_taxon_dict():
    taxonDict = {}
    with open(args.taxonomy) as silvaTaxonomy:
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
    with open(args.fasta, "r") as silva, open(args.output, "a") as output:
        for record in SeqIO.parse(silva, "fasta"):
            accession = str(record.id).split(".")[0]
            #print accession
            newHeader = ">silva|"+str(record.id)+"|"+taxonDict[accession]+"\n"
            output.write(newHeader+str(record.seq)+"\n")

def main():
    add_taxonomy(make_taxon_dict())

if __name__ == "__main__":
    main()
