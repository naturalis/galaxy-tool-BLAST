#!/usr/bin/python
"""
blastn_add_taxonomy   V1.0    martenhoogeveen@naturalis.nl
This script adds the taxonomy to the BLAST output. The input is de folder path that contains the blast results.
"""
import json, sys, argparse, os, glob, requests
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

def check_merged_taxonomy(taxid, mergedTaxonDict):
    try:
        a = mergedTaxonDict[taxid]
        return a
    except:
        return "N/A"

def find_genbank_taxonomy(hit, taxonomyDict, mergedTaxonDict):
    taxid = hit.split("\t")[3]
    if taxid == "N/A":
        return hit.strip() + "\tGenbank\t" + "unknown kingdom / unknown phylum / unknown class / unknown order / unknown family / unknown genus / unknown species\n"
    else:
        taxonomydb = taxonomyDict
        try:
            kingdom = taxonomydb[taxid]["kingdom"]
            superkingdom = taxonomydb[taxid]["superkingdom"]
        except KeyError:
            mergedTaxid = check_merged_taxonomy(taxid, mergedTaxonDict)
            if mergedTaxid != "N/A":
                taxid = mergedTaxid
                kingdom = taxonomydb[mergedTaxid]["kingdom"]
                superkingdom = taxonomydb[mergedTaxid]["superkingdom"]

        if kingdom and kingdom != "unknown kingdom":
            return hit.strip() + "\tGenbank\t" + taxonomydb[taxid]["kingdom"] + " / " + taxonomydb[taxid]["phylum"] + " / " + taxonomydb[taxid]["class"] + " / " + taxonomydb[taxid]["order"] + " / " + taxonomydb[taxid]["family"] + " / " + taxonomydb[taxid]["genus"] + " / " + taxonomydb[taxid]["species"] + "\n"
        elif superkingdom and superkingdom != "unknown superkingdom":
            return hit.strip() + "\tGenbank\t" + taxonomydb[taxid]["superkingdom"] + " / " + taxonomydb[taxid]["phylum"] + " / " + taxonomydb[taxid]["class"] + " / " + taxonomydb[taxid]["order"] + " / " + taxonomydb[taxid]["family"] + " / " + taxonomydb[taxid]["genus"] + " / " + taxonomydb[taxid]["species"] + "\n"
        else:
            return hit.strip() + "\tGenbank\t" + taxonomydb[taxid]["kingdom"] + " / " + taxonomydb[taxid]["phylum"] + " / " + taxonomydb[taxid]["class"] + " / " + taxonomydb[taxid]["order"] + " / " + taxonomydb[taxid]["family"] + " / " + taxonomydb[taxid]["genus"] + " / " + taxonomydb[taxid]["species"] + "\n"

def get_kingdom(knownTaxons):
    kingdom = "unknown kingdom"
    for taxon in knownTaxons:
        if "unknown" not in taxon:
            rec = requests.get("http://resolver.globalnames.org/name_resolvers.json", params={"names": taxon}, allow_redirects=True)
            if rec.text:
                a = json.loads(rec.text)
                globalNamesResult = {}
                try:
                    for x in a["data"][0]["results"]:
                        if x["data_source_title"] not in globalNamesResult:
                            globalNamesResult[x["data_source_title"]] = x
                    if "GBIF Backbone Taxonomy" in globalNamesResult:
                        kingdom = globalNamesResult["GBIF Backbone Taxonomy"]["classification_path"].split("|")[0]
                        return kingdom
                    elif "Catalogue of Life" in globalNamesResult:
                        kingdom = globalNamesResult["Catalogue of Life"]["classification_path"].split("|")[0]
                        return kingdom
                except KeyError:
                    pass
        return kingdom

def find_bold_taxonomy(line):
    boldId = line.split("\t")[1].split("|")[1]
    rec = requests.get("http://www.boldsystems.org/index.php/API_Public/specimen",params={"ids": boldId, "format":"json"}, allow_redirects=True)
    if rec.text:
        a = json.loads(rec.text)
        if len(a["bold_records"]["records"]) == 1:
            for x in a["bold_records"]["records"]:
                try:
                    phylum = a["bold_records"]["records"][x]["taxonomy"]["phylum"]["taxon"]["name"]
                except KeyError:
                    phylum = "unknown phylum"
                try:
                    class_taxon = a["bold_records"]["records"][x]["taxonomy"]["class"]["taxon"]["name"]
                except KeyError:
                    class_taxon = "unknown class"
                try:
                    order = a["bold_records"]["records"][x]["taxonomy"]["order"]["taxon"]["name"]
                except KeyError:
                    order = "unknown order"
                try:
                    family = a["bold_records"]["records"][x]["taxonomy"]["family"]["taxon"]["name"]
                except KeyError:
                    family = "unknown family"
                try:
                    genus = a["bold_records"]["records"][x]["taxonomy"]["genus"]["taxon"]["name"]
                except KeyError:
                    genus = "unknown genus"
                try:
                    species = a["bold_records"]["records"][x]["taxonomy"]["species"]["taxon"]["name"]
                except KeyError:
                    species = "unknown species"
        else:
            return line.strip() + "\t" +"something went wrong, more than one record found\n"
        kingdom = get_kingdom([phylum, class_taxon, order, family])
        taxonomy = " / ".join([kingdom, phylum, class_taxon, order, family, genus, species])
        return line.strip() + "\tBOLD\t" + taxonomy+"\n"
    else:
        return line.strip() +"\tBOLD\tunknown kingdom / unknown phylum / unknown class / unknown order / unknown family / unknown genus / unknown species\n"

def find_private_bold_taxonomy(line):
    taxonomyList = line.split("\t")[1].split("|")
    species = taxonomyList[-1] if taxonomyList[-1] else "unknown species"
    genus = taxonomyList[-2] if taxonomyList[-2] else "unknown genus"
    family = taxonomyList[-3] if taxonomyList[-3] else "unknown family"
    order = taxonomyList[-4] if taxonomyList[-4] else "unknown order"
    classe = taxonomyList[-5] if taxonomyList[-5] else "unknown class"
    phylum = taxonomyList[-6] if taxonomyList[-6] else "unknown phylum"
    kingdom = get_kingdom([phylum, classe, order, family])
    taxonomy = [kingdom, phylum, classe, order, family, genus, species]
    return line.strip() + "\tprivate_BOLD\t" + " / ".join(taxonomy) + "\n"


def find_gbif_taxonomy(line):
    splitLine = line.split("\t")
    species = line.split("\t")[-1].split(" / ")[-1]
    genus = line.split("\t")[-1].split(" / ")[-2]
    if "unknown" not in species:
        searchWord = species.split(" ")[0] + species.split(" ")[1]
    elif "unknown" not in genus:
        searchWord = genus
    else:
        return line

    rec = requests.get("http://resolver.globalnames.org/name_resolvers.json", params={"names": searchWord}, allow_redirects=True)
    if rec.text:
        a = json.loads(rec.text)
        globalNamesResult = {}
        try:
            for x in a["data"][0]["results"]:
                if x["data_source_title"] not in globalNamesResult:
                    globalNamesResult[x["data_source_title"]] = x
            if "GBIF Backbone Taxonomy" in globalNamesResult:
                taxonomy = globalNamesResult["GBIF Backbone Taxonomy"]["classification_path"].split("|")
                source = "GBIF"
                unknown_list = ["unknown kingdom", "unknown phylum", "unknown class", "unknown order", "unknown family", "unknown genus", "unknown species"]
                for unknown in unknown_list[len(taxonomy):]:
                    taxonomy.append(unknown)
                taxonomy = " / ".join(taxonomy)
            elif "Catalogue of Life" in globalNamesResult:
                taxonomy = globalNamesResult["Catalogue of Life"]["classification_path"].split("|")
                source = "Catalogue of Life"
                unknown_list = ["unknown kingdom", "unknown phylum", "unknown class", "unknown order", "unknown family", "unknown genus", "unknown species"]
                for unknown in unknown_list[len(taxonomy):]:
                    taxonomy.append(unknown)
                taxonomy = " / ".join(taxonomy)
            else:
                source = "Original"
                taxonomy = splitLine[-1]
            splitLine[-2] = source
            splitLine[-1] = taxonomy
            return "\t".join(splitLine)
        except:
            source = "Original"
            taxonomy = splitLine[-1]
            splitLine[-2] = source
            splitLine[-1] = taxonomy
            return "\t".join(splitLine)
    else:
        return line

def add_taxonomy(file, taxonomyDict, mergedTaxonDict):
    with open(file, "r") as blasthits, open(args.blastinputfolder.strip() + "/taxonomy_"+ os.path.basename(file), "a") as output:
        line_taxonomy = ""
        for line in blasthits:
            if line.split("\t")[1].split("|")[0] == "BOLD":
                line_taxonomy = find_bold_taxonomy(line)
            elif line.split("\t")[1].split("|")[0] == "private_BOLD":
                line_taxonomy = find_private_bold_taxonomy(line)
            else:
                line_taxonomy = find_genbank_taxonomy(line, taxonomyDict, mergedTaxonDict)
            if args.taxonomy_source == "GBIF":
                line_taxonomy = find_gbif_taxonomy(line_taxonomy)
                output.write(line_taxonomy.strip()+"\n")
            elif args.taxonomy_source == "default":
                output.write(line_taxonomy)

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