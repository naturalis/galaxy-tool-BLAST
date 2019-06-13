#!/usr/bin/python
"""
Add header en filter on coverage, simple script for the example on github  V1.0    martenhoogeveen@naturalis.nl
"""
import sys, argparse, os, glob, string
from Bio import SeqIO
from subprocess import call, Popen, PIPE

# Retrieve the commandline arguments
parser = argparse.ArgumentParser(description='')
parser.add_argument('-i', '--input', dest='input', type=str,help='blast format inputfile', required=True)
parser.add_argument('-cov', dest='coverage', type=str, required=False, nargs='?', default="0")
args = parser.parse_args()

def coverage_filter():
    with open(args.input+"_covfiltered.tabular", "a") as headLine:
        headLine.write("#Query ID\t#Subject\t#Subject accession\t#Subject Taxonomy ID\t#Identity percentage\t#Coverage\t#evalue\t#bitscore\n")
    with open(args.input, "r") as blast, open(args.input+"_covfiltered.tabular", "a") as output:
        for hit in blast:
            coverage = hit.split("\t")[5]
            if float(coverage) >= float(args.coverage):
                output.write(hit)
    #Popen(["rm", blastfile], stdout=PIPE, stderr=PIPE).communicate()
    #Popen(["mv", blastfile+"_cov", blastfile], stdout=PIPE, stderr=PIPE).communicate()

def main():
    coverage_filter()


if __name__ == "__main__":
    main()
