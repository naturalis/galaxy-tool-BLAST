class Silva:
    def find_silva_taxonomy(self, line):
        taxonomyList = line.split("\t")[1].split("|")[-1].split(";")

        species = taxonomyList[-1]
        if species == "unidentified":
            species = "unknown species"
        ranks = taxonomyList[:-1]
        unknowns = ["unknown kingdom", "unknown phylum", "unknown class", "unknown order", "unknown family", "unknown genus"]
        for x in unknowns[len(ranks):]:
            ranks.append(x)
        ranks.append(species)
        print ranks
        species = ranks[6]
        genus = ranks[5]
        family = ranks[4]
        order = ranks[3]
        classe = ranks[2]
        phylum = ranks[1]
        kingdom = ranks[0]
        taxonomy = [kingdom, phylum, classe, order, family, genus, species]

        newLine = line.strip().split("\t")
        newLine[1] = newLine[1].split("|")[1]
        newLine[2] = newLine[2].split("|")[1].split(".")[0]
        return "\t".join(newLine) + "\tsilva\t" + " / ".join(taxonomy) + "\n"
