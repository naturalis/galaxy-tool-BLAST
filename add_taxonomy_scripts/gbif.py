
import sqlite3

class Gbif:
    def __init__(self, database):
        self.db = sqlite3.connect(database)
        self.cursor = self.db.cursor()

    def find_gbif_taxonomy(self, line):
        species = line.split("\t")[-1].split(" / ")[-1].strip()
        genus = line.split("\t")[-1].split(" / ")[-2]
        family = line.split("\t")[-1].split(" / ")[-3]
        hit = None
        if "unknown" not in species and int(species.count(" ")) >= 1:
            self.cursor.execute("SELECT * FROM gbif WHERE species=? LIMIT 1", [species.split(" ")[0] + " " + species.split(" ")[1].strip()])
            hit = self.cursor.fetchone()
            if hit is not None and hit[4] == "synonym" and hit[4] == "homotypic synonym":
                self.cursor.execute("SELECT * FROM gbif WHERE taxonID=? LIMIT 1", [hit[3]])
                hit = self.cursor.fetchone()
            if hit is not None:
                line = line.split("\t")
                line[-1] = " / ".join(list(reversed(hit[5:12])))
                line[-2] = hit[1]
                return "\t".join(line)

        if "unknown" not in genus and hit is None:
            self.cursor.execute("SELECT species, genus, family, order1, class, phylum, kingdom FROM gbif WHERE genus=? LIMIT 1", [genus.strip()])
            hit = self.cursor.fetchone()
            if hit is not None:
                line = line.split("\t")
                unknown = ["unknown species"]
                taxonomy = list(reversed(hit[1:]))+unknown
                line[-1] = " / ".join(taxonomy)
                #line[-2] = hit[1]
                line[-2] = "gbif"
                return "\t".join(line)

        if "unknown" not in family and hit is None:
            self.cursor.execute("SELECT species, genus, family, order1, class, phylum, kingdom FROM gbif WHERE family=? LIMIT 1", [family.strip()])
            hit = self.cursor.fetchone()
            if hit is not None:
                line = line.split("\t")
                unknown = ["unknown genus", "unknown species"]
                taxonomy = list(reversed(hit[2:]))+unknown
                #print taxonomy
                line[-1] = " / ".join(taxonomy)
                #line[-2] = hit[1]
                line[-2] = "gbif"
                return "\t".join(line)

        if hit is None:
            return line