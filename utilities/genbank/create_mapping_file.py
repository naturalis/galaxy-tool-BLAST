"""

"""
from Bio import SeqIO
import sys, os, argparse
from subprocess import call, Popen, PIPE
# Retrieve the commandline arguments
parser = argparse.ArgumentParser(description='Create taxonid mapping file for a specific fasta file')
parser.add_argument('-f', dest='inputfasta', type=str, required=True)
parser.add_argument('-m', '--taxidmap', dest='taxidmap', type=str, required=True)
parser.add_argument('-o', '--output', dest='output', type=str, required=True)
args = parser.parse_args()

accessions = {}

#print "start making accession dict"
with open(args.inputfasta, "rU") as handle:
    for record in SeqIO.parse(handle, "fasta"):
        accession = str(record.id)
        try:
            accessions[accession]=accession
        except:
            pass
#print "start making accession dict - done"

with open(args.taxidmap, "rU") as taxonmap, open(args.output,'a') as newmap:
    for x in taxonmap:
        mapaccession = x.split(" ")[0].strip()
        try:
            newmap.write(accessions[mapaccession]+" "+x.split(" ")[1])
        except:
            pass
