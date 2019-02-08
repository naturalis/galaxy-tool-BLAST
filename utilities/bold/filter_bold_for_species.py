"""
"""
from Bio import SeqIO
import argparse

parser = argparse.ArgumentParser(description='Filter BOLD fasta file for species level only')
parser.add_argument('-b', '--bold_fasta', dest='bold', type=str, required=True)
parser.add_argument('-o', '--output', dest='output', type=str, required=True)
args = parser.parse_args()

def check_taxonomy():
    with open(args.bold, "r") as bold, open(args.output,"a") as output:
        for record in SeqIO.parse(bold, "fasta"):
            if "unknown" not in str(record.description).strip().split("|")[-1] and "unknown" not in str(record.description).strip().split("|")[-2]:
                output.write(">"+str(record.description).strip()+"\n")
                output.write(str(record.seq)+"\n")

def main():
    check_taxonomy()

if __name__=="__main__":
    main()
