#!/usr/bin/python
import sys, os, argparse
from subprocess import call, Popen, PIPE, check_output

# Retrieve the commandline arguments
parser = argparse.ArgumentParser(description='Filter the NCBI nt database')
parser.add_argument('-t', '--taxidlineage', dest='taxidlineage', type=str, required=True)
parser.add_argument('-i', '--taxonid', dest='taxonid', type=str, required=True)
parser.add_argument('-a', '--accession2taxid', dest='accession2taxid', type=str, required=True)
parser.add_argument('-o', '--output', dest='output', type=str, required=True)
args = parser.parse_args()

def read_taxidlineage():
    taxonids = set({})
    grep = Popen(["grep", "-w", args.taxonid, args.taxidlineage],stdout=PIPE)
    output = Popen(['awk', '{print $1}'], stdin=grep.stdout, stdout=PIPE)
    for line in output.stdout:
        taxonids.add(line.strip())
    return taxonids

def get_accessions(taxonids):
    with open(args.output, "a") as bulk_entry:
        accession = Popen(["cat", args.accession2taxid], stdout=PIPE)
        for line in accession.stdout:
            if line.strip().split("\t")[0] != "accession":
                if line.strip().split("\t")[2] in taxonids:
                    bulk_entry.write(line.strip().split("\t")[1]+"\n")

def main():
    taxonids = read_taxidlineage()
    get_accessions(taxonids)

if __name__ == "__main__":
    main()
