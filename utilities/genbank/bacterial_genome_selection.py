from Bio import SeqIO
import sys, os, argparse
from subprocess import call, Popen, PIPE
# Retrieve the commandline arguments
parser = argparse.ArgumentParser(description='Extract bacterial genome sequences from NCBI nt database')
parser.add_argument('-db', dest='db', type=str, required=True)
parser.add_argument('-a', '--accessions', dest='accessions', type=str, required=True)
parser.add_argument('-o', '--output', dest='output', type=str, required=True)
args = parser.parse_args()

def read_accessions():
    #accessionList = []
    accessionSet = set()
    with open(args.accessions, "r") as accessionFile:
        for x in accessionFile:
            accessionSet.add(x.strip())
    return accessionSet

def select_bac(accessionSet):
    with open(args.db, "rU") as handle, open(args.output,'a') as newgenome:
        for record in SeqIO.parse(handle, "fasta"):
            if str(record.id) in accessionSet and "genome" in str(record.description.lower()):
                newgenome.write(">"+str(record.description)+"\n"+str(record.seq)+"\n")


if __name__ == '__main__':
    select_bac(read_accessions())

#    for record in SeqIO.parse(handle, "fasta"):
#        if "genome" in str(record.description.lower()):
            #newgenome.write(">"+str(record.description)+"\n")
            #newgenome.write(str(record.seq)+"\n")
