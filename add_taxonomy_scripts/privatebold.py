import sqlite3

class PrivateBold:

    def find_private_bold_taxonomy(self, line):
        species = line.split("\t")[1].split("|")[2]
        genus = line.split("\t")[1].split("|")[8]
        family = line.split("\t")[1].split("|")[7]
        order = line.split("\t")[1].split("|")[6]
        classe = line.split("\t")[1].split("|")[5]
        phylum = line.split("\t")[1].split("|")[4]
        kingdom = line.split("\t")[1].split("|")[3]
        taxonomy = [kingdom, phylum, classe, order, family, genus, species]
        newLine = line.strip().split("\t")
        newLine[1] = newLine[1].split("|")[1]
        newLine[2] = newLine[2].split("|")[1]
        return "\t".join(newLine) + "\tprivate\t" + " / ".join(taxonomy) + "\n"
