#!/usr/bin/python
"""
blastn_add_taxonomy   V1.0    martenhoogeveen@naturalis.nl
This script adds the taxonomy to the BLAST output. The input is de folder path that contains the blast results.
"""
import json, sys, argparse, os, glob
from add_taxonomy_scripts.genbank import Genbank
from add_taxonomy_scripts.gbif import Gbif
from add_taxonomy_scripts.bold import Bold
from add_taxonomy_scripts.privatebold import PrivateBold
from add_taxonomy_scripts.unite import Unite
from add_taxonomy_scripts.silva import Silva

# Retrieve the commandline arguments
parser = argparse.ArgumentParser(description='Add taxonomy to BLAST output')
parser.add_argument('-i', '--blast_input_file', metavar='input file with BLAST custom outfmt 6 output', dest='blastinputfile', type=str, required=True)
parser.add_argument('-t', '--taxonomy_reference', metavar='taxonomy reference', dest='rankedlineage', type=str, required=False, nargs='?', default="taxonomy_reference.json")
parser.add_argument('-m', '--merged', metavar='merged taxonids', dest='merged', type=str, help='merged taxon id json', required=False, nargs='?', default="merged_taxonomy.json")
parser.add_argument('-ts', '--taxonomy_source', dest='taxonomy_source', type=str, required=False, nargs='?', default="default")
parser.add_argument('-o', '--output', metavar='output', dest='output', type=str, help='output file, BLAST hits with taxonomy', required=False, nargs='?', default="")
args = parser.parse_args()

def add_taxonomy(genbank, bold, privatebold, unite, silva):
    with open(args.blastinputfile, "r") as blasthits, open("taxonomy_"+ os.path.basename(args.blastinputfile), "a") as output:
        for line in blasthits:
            if line.split("\t")[0] == "#Query ID":
                output.write(line.strip()+"\t#Source\t#Taxonomy\n")
            else:
                if line.split("\t")[1].split("|")[0] == "BOLD":
                    line_taxonomy = bold.find_bold_taxonomy(line, "bold")
                elif line.split("\t")[1].split("|")[0] == "klasse":
                    line_taxonomy = bold.find_bold_taxonomy(line, "klasse")
                elif line.split("\t")[1].split("|")[0] == "private_BOLD":
                    line_taxonomy = privatebold.find_private_bold_taxonomy(line)
                elif line.split("\t")[1].split("|")[0] == "UNITE":
                    line_taxonomy = unite.find_unite_taxonomy(line)
                elif line.split("\t")[1].split("|")[0] == "silva":
                    line_taxonomy = silva.find_silva_taxonomy(line)
                else:
                    line_taxonomy = genbank.find_genbank_taxonomy(line)

                output.write(line_taxonomy.encode('utf-8').strip()+"\n")

def process_files():
    genbank = Genbank(args.rankedlineage, args.merged)
    bold = Bold()
    privatebold = PrivateBold()
    unite = Unite()
    silva = Silva()
    add_taxonomy(genbank, bold, privatebold, unite, silva)

def main():
    process_files()




if __name__ == "__main__":
    main()
