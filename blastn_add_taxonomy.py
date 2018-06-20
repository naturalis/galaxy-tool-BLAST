#!/usr/bin/python
"""
blastn_add_taxonomy   V1.0    martenhoogeveen@naturalis.nl
This script adds the taxonomy to the BLAST output. The input is de folder path that contains the blast results.
"""
import json, sys, argparse, os, glob
# Retrieve the commandline arguments
parser = argparse.ArgumentParser(description='Add taxonomy to BLAST output')
parser.add_argument('-i', '--blast_input_folder', metavar='input folder with BLAST custom outfmt 6 output', dest='blastinputfolder', type=str,help='input folder', required=True)
parser.add_argument('-t', '--taxonomy_reference', metavar='taxonomy reference', dest='rankedlineage', type=str, help='reference json taxonomy file', required=False, nargs='?', default="taxonomy_reference.json")
parser.add_argument('-m', '--merged', metavar='merged taxonids', dest='merged', type=str, help='merged taxon id json', required=False, nargs='?', default="merged_taxonomy.json")
parser.add_argument('-ts', '--taxonomy_source', dest='taxonomy_source', type=str, required=False, nargs='?', default="default")
parser.add_argument('-o', '--output', metavar='output', dest='output', type=str, help='output file, BLAST hits with taxonomy', required=False, nargs='?', default="")
args = parser.parse_args()

def merged_taxonomy():
    mergedDict = {}
    with open(args.merged) as merged:
        for taxid in merged:
            a = map(str.strip, taxid.split("|"))
            mergedDict[a[0]]=a[1]
    return mergedDict

def reference_taxonomy():
    taxonomyDict = {}
    with open(args.rankedlineage) as rankedlineage:
        for tax in rankedlineage:
            tax = tax.split("|")
            taxonid = tax[0]
            species = tax[1].strip() if tax[1].strip() else "unknown species"
            genus = tax[3].strip() if tax[3].strip() else "unknown genus"
            family = tax[4].strip() if tax[4].strip() else "unknown family"
            order = tax[5].strip() if tax[5].strip() else "unknown order"
            classe = tax[6].strip() if tax[6].strip() else "unknown class"
            phylum = tax[7].strip() if tax[7].strip() else "unknown phylum"
            kingdom = tax[8].strip() if tax[8].strip() else "unknown kingdom"
            superkingdom = tax[9].strip() if tax[9].strip() else "unknown superkingdom"
            taxonomyDict[str(tax[0].strip())] = {"species":species, "genus":genus, "family":family, "order":order, "class":classe, "phylum":phylum, "kingdom":kingdom,"superkingdom":superkingdom}
    return taxonomyDict


def find_genbank_taxonomy(hit, taxonomyDict, mergedTaxonDict):
    taxid = hit.split("\t")[3]
    if taxid == "N/A":
        return hit.strip() + "\t" + "unknown kingdom / unknown phylum / unknown class / unknown order / family / genus / species\n"
    else:
        taxonomydb = taxonomyDict
        try:
            kingdom = taxonomydb[taxid]["kingdom"]
            superkingdom = taxonomydb[taxid]["superkingdom"]
        except KeyError:
            taxid = check_merged_taxonomy(taxid, mergedTaxonDict)
            kingdom = taxonomydb[taxid]["kingdom"]
            superkingdom = taxonomydb[taxid]["superkingdom"]

        if kingdom and kingdom != "unknown kingdom":
            return hit.strip() + "\t" + taxonomydb[taxid]["kingdom"] + " / " + taxonomydb[taxid]["phylum"] + " / " + taxonomydb[taxid]["class"] + " / " + taxonomydb[taxid]["order"] + " / " + taxonomydb[taxid]["family"] + " / " + taxonomydb[taxid]["genus"] + " / " + taxonomydb[taxid]["species"] + "\n"
        elif superkingdom and superkingdom != "unknown superkingdom":
            return hit.strip() + "\t" + taxonomydb[taxid]["superkingdom"] + " / " + taxonomydb[taxid]["phylum"] + " / " + taxonomydb[taxid]["class"] + " / " + taxonomydb[taxid]["order"] + " / " + taxonomydb[taxid]["family"] + " / " + taxonomydb[taxid]["genus"] + " / " + taxonomydb[taxid]["species"] + "\n"
        else:
            return hit.strip() + "\t" + taxonomydb[taxid]["kingdom"] + " / " + taxonomydb[taxid]["phylum"] + " / " + taxonomydb[taxid]["class"] + " / " + taxonomydb[taxid]["order"] + " / " + taxonomydb[taxid]["family"] + " / " + taxonomydb[taxid]["genus"] + " / " + taxonomydb[taxid]["species"] + "\n"


def add_taxonomy(file, taxonomyDict, mergedTaxonDict):
    with open(file) as blasthits, open(args.blastinputfolder.strip() + "/taxonomy_"+ os.path.basename(file), "a") as output:
        for line in blasthits:
            if line.split("\t")[1].split("|")[0] == "BOLD":
                pass
            else:
                print find_genbank_taxonomy(line, taxonomyDict, mergedTaxonDict)
            if args.taxonomy_source == "BGIF":
                pass
            if args.taxonomy_source == "default":
                pass#write

def process_files(taxonomyDict, mergedTaxonDict):
    files = [x for x in sorted(glob.glob(args.blastinputfolder.strip() + "/*.tabular"))]
    for file in files:
        add_taxonomy(file, taxonomyDict, mergedTaxonDict)

def main():
    taxonomyDict = reference_taxonomy()
    mergedTaxonDict = merged_taxonomy()
    process_files(taxonomyDict, mergedTaxonDict)




if __name__ == "__main__":
    main()