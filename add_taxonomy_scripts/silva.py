class Silva:
    def find_silva_taxonomy(self, line):
        print line.split("\t")[2]
        taxonomyList = line.split("\t")[1].split(" ", 1)[-1].split(";")

        species = taxonomyList[-1] if taxonomyList[-1] else "unknown species"
        species = species.replace("_", " ")
        genus = taxonomyList[-2] if taxonomyList[-2] else "unknown genus"
        family = taxonomyList[-3] if taxonomyList[-3] else "unknown family"
        order = taxonomyList[-4] if taxonomyList[-4] else "unknown order"
        classe = taxonomyList[-5] if taxonomyList[-5] else "unknown class"
        phylum = taxonomyList[-6] if taxonomyList[-6] else "unknown phylum"
        kingdom = taxonomyList[-7] if taxonomyList[-7] else "unknown kingdom"
        taxonomy = [kingdom, phylum, classe, order, family, genus, species]

        newLine = line.strip().split("\t")
        newLine[1] = newLine[1].split(" ", 1)[0]
        newLine[2] = newLine[1].split("|")[1]
        return "\t".join(newLine) + "\tsilva\t" + " / ".join(taxonomy) + "\n"
