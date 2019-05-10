import sqlite3

class Bold:
    def __init__(self, database, gbif):
        self.db = database
        self.gbif_db = gbif

    def find_bold_taxonomy(self, line, source):
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
        return "\t".join(newLine) + "\t"+source+"\t" + " / ".join(taxonomy) + "\n"
    """
    def __init__(self, database, gbif):
        self.db = sqlite3.connect(database)
        self.cursor = self.db.cursor()
        self.gbif_db = sqlite3.connect(gbif)
        self.gbif_cursor = self.gbif_db.cursor()

    def find_bold_taxonomy(self, line):
        boldAccession = line.split("\t")[1].split("|")[1]
        self.cursor.execute("SELECT * FROM bold WHERE processid=? LIMIT 1", [boldAccession])
        hit = self.cursor.fetchone()
        if hit is not None:
            line = line.split("\t")
            line = map(str.strip, line)
            line.append(hit[1])
            kingdom = self.get_kingdom({"phylum":hit[8], "class":hit[7], "order1":hit[6], "family":hit[5]})
            line.append(" / ".join(list(reversed(list(hit[3:9])+[kingdom]))))
            return "\t".join(line)
        else:
            a = line.strip()+"\tBOLD\t" + "unknown kingdom / unknown phylum / unknown class / unknown order / unknown family / unknown genus / unknown species"
            return a

    def get_kingdom(self, taxons):
        kingdom = "unknown kingdom"
        for taxon in taxons:
            if "unknown" not in taxons[taxon]:
                self.gbif_cursor.execute("SELECT kingdom FROM gbif WHERE "+taxon+"=? LIMIT 1", [taxons[taxon]])
                hit = self.gbif_cursor.fetchone()
                if hit is not None:
                    return hit[0]
        return kingdom
    """
