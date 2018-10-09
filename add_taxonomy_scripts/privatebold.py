import sqlite3

class PrivateBold:
    def __init__(self, gbif):
        self.gbif_db = sqlite3.connect(gbif)
        self.gbif_cursor = self.gbif_db.cursor()

    def find_private_bold_taxonomy(self, line):
        taxonomyList = line.split("\t")[1].split("|")
        species = taxonomyList[-1] if taxonomyList[-1] else "unknown species"
        genus = taxonomyList[-2] if taxonomyList[-2] else "unknown genus"
        species = "unknown species" if species == genus else species
        family = taxonomyList[-3] if taxonomyList[-3] else "unknown family"
        order = taxonomyList[-4] if taxonomyList[-4] else "unknown order"
        classe = taxonomyList[-5] if taxonomyList[-5] else "unknown class"
        phylum = taxonomyList[-6] if taxonomyList[-6] else "unknown phylum"
        kingdom = self.get_kingdom({"phylum": phylum, "class": classe, "order1": order, "family": family})
        taxonomy = [kingdom, phylum, classe, order, family, genus, species]
        return line.strip() + "\tprivate_BOLD\t" + " / ".join(taxonomy) + "\n"

    def get_kingdom(self, taxons):
        kingdom = "unknown kingdom"
        for taxon in taxons:
            if "unknown" not in taxons[taxon]:
                self.gbif_cursor.execute("SELECT kingdom FROM gbif WHERE " + taxon + "=? LIMIT 1", [taxons[taxon]])
                hit = self.gbif_cursor.fetchone()
                if hit is not None:
                    return hit[0]
        return kingdom
