"""
"""
from Bio import SeqIO
import argparse

parser = argparse.ArgumentParser(description='Add taxonomy to BOLD fasta file')
parser.add_argument('-t', '--taxonomy', dest='taxonomy', type=str, required=True)
parser.add_argument('-g', '--gbif_taxonomy', dest='gbif', type=str, required=True)
parser.add_argument('-b', '--bold_fasta', dest='bold', type=str, required=True)
parser.add_argument('-o', '--output', dest='output', type=str, required=True)
args = parser.parse_args()

def make_taxon_dict():
    taxonDict = {}
    with open(args.taxonomy,"r") as taxonomy:
        for x in taxonomy:
            x = x.strip().split("\t")
            unknowns = ["unknown kingdom", "unknown phylum", "unknown class", "unknown order", "unknown family", "unknown genus", "unknown species"]
            for known in unknowns[len(x):]:
                x.append(known)
            valueCount = 0
            for value in x:
                if not value:
                    x[valueCount] = unknowns[valueCount]
                valueCount += 1
            taxonDict[x[0]] = x
    return taxonDict

def make_kingdom_dict():
    kingdomDict = {}
    with open(args.gbif,"r") as gbif:
        for x in gbif:
            x = x.split("\t")
            if x[1] not in kingdomDict:
                kingdomDict[x[1]] = x[0]
            if x[2] not in kingdomDict:
                kingdomDict[x[2]] = x[0]
            if x[3] not in kingdomDict:
                kingdomDict[x[3]] = x[0]
            if x[4] not in kingdomDict:
                kingdomDict[x[4]] = x[0]
            if x[5] not in kingdomDict:
                kingdomDict[x[5]] = x[0]
    return kingdomDict


def add_taxonomy(taxonDict, kingdomDict):
    with open(args.bold, "r") as bold, open(args.output,"a") as output:
        for record in SeqIO.parse(bold, "fasta"):
            accession = str(record.description).split("|")[0]
            if accession in taxonDict:
                if taxonDict[accession][1] in kingdomDict:
                    kingdom = kingdomDict[taxonDict[accession][1]]
                elif taxonDict[accession][2] in kingdomDict:
                    kingdom = kingdomDict[taxonDict[accession][2]]
                elif taxonDict[accession][3] in kingdomDict:
                    kingdom = kingdomDict[taxonDict[accession][3]]
                elif taxonDict[accession][4] in kingdomDict:
                    kingdom = kingdomDict[taxonDict[accession][4]]
                elif taxonDict[accession][5] in kingdomDict:
                    kingdom = kingdomDict[taxonDict[accession][5]]
                else:
                    #print accession+" no kingdom"
                    kingdom = "unknown kingdom"
                output.write(">BOLD|"+accession+"|"+taxonDict[accession][-1]+"|"+kingdom+"|"+taxonDict[accession][1]+"|"+taxonDict[accession][2]+"|"+taxonDict[accession][3]+"|"+taxonDict[accession][4]+"|"+taxonDict[accession][5]+"|"+taxonDict[accession][-1]+"\n")
                output.write(str(record.seq)+"\n")
            else:
                print accession+" no taxonomy"

def main():
    taxonDict = make_taxon_dict()
    kingdomDict = make_kingdom_dict()
    add_taxonomy(taxonDict, kingdomDict)

if __name__=="__main__":
    main()
