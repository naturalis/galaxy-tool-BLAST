import sqlite3
db = sqlite3.connect('taxonomy_db2')
cursor = db.cursor()

def make_database():
    cursor.execute('''CREATE TABLE gbif(id INTEGER PRIMARY KEY, source TEXT, taxonID INTEGER, acceptedNameUsageID INTEGER, taxonomicStatus TEXT, species TEXT, genus TEXT, family TEXT, order1 TEXT, class TEXT, phylum TEXT, kingdom TEXT)''')
    db.commit()

def check_empty_values(data):
    a = 0
    for taxon in data:
        a += 2 if not data["taxonID"] else 0
        a += 2 if not data["taxonomicStatus"] else 0
        a += 2 if not data["species"] else 0
        a += 2 if not data["genus"] else 0
        a += 1 if not data["family"] else 0
        a += 1 if not data["order1"] else 0
        a += 1 if not data["class"] else 0
        a += 1 if not data["phylum"] else 0
        a += 1 if not data["kingdom"] else 0
    if a >= 2:
        return False
    else:
        return  True

def check_unknowns(data):
    for x in data:
        if not data[str(x)]:
            data[str(x)] = "unknown "+str(x)
    return data

def add_gbif_backbone_taxonomy():
    genusSet = set()
    with open("Taxon.tsv", "r") as gbif:
        for line in gbif:
            line = line.split("\t")
            data = {"source":"gbif", "taxonID":line[0], "acceptedNameUsageID":line[3], "taxonomicStatus":line[14], "species":line[7], "genus":line[8].strip(), "family":line[21], "order1":line[20],"class":line[19], "phylum":line[18], "kingdom":line[17]}
            data = {x.decode('utf8'): v.decode('utf8') for x, v in data.items()}
            emptyCheck = check_empty_values(data)
            data = check_unknowns(data)
            if line[11] == "species" and emptyCheck:
                genusSet.add(line[8].strip())
                cursor.execute('''INSERT INTO gbif(source, taxonID, acceptedNameUsageID, taxonomicStatus, species, genus, family, order1, class, phylum, kingdom)VALUES(:source, :taxonID, :acceptedNameUsageID, :taxonomicStatus, :species, :genus, :family, :order1, :class, :phylum, :kingdom)''', data)
    #db.commit()
    with open("Taxon.tsv", "r") as gbif:
        for line in gbif:
            line = line.split("\t")
            data = {"source":"gbif", "taxonID":line[0], "acceptedNameUsageID":line[3], "taxonomicStatus":line[14], "species":line[7], "genus":line[8].strip(), "family":line[21], "order1":line[20],"class":line[19], "phylum":line[18], "kingdom":line[17]}
            data = {x.decode('utf8'): v.decode('utf8') for x, v in data.items()}
            emptyCheck = check_empty_values(data)
            data = check_unknowns(data)
            if line[11] == "genus" and line[8].strip() not in genusSet and emptyCheck:
                genusSet.add(line[8].strip())
                data[7] = "unknown species"
                cursor.execute('''INSERT INTO gbif(source, taxonID, acceptedNameUsageID, taxonomicStatus, species, genus, family, order1, class, phylum, kingdom)VALUES(:source, :taxonID, :acceptedNameUsageID, :taxonomicStatus, :species, :genus, :family, :order1, :class, :phylum, :kingdom)''', data)

    db.commit()

def add_catalog_of_life_taxonomy():
    genusSet = set()
    with open("taxa.txt", "r") as catalog_of_life:
        for line in catalog_of_life:
            line = line.split("\t")
            data = {"source":"catalog of life", "taxonID":line[0], "acceptedNameUsageID":line[4], "taxonomicStatus":line[6], "species":line[17]+" "+line[19], "genus":line[17].strip(), "family":line[15], "order1":line[13], "class":line[12], "phylum":line[11], "kingdom":line[10]}
            data = {x.decode('utf8'): v.decode('utf8') for x, v in data.items()}
            emptyCheck = check_empty_values(data)
            data = check_unknowns(data)
            if line[7] == "species" and emptyCheck:
                genusSet.add(line[19].strip())
                cursor.execute('''INSERT INTO gbif(source, taxonID, acceptedNameUsageID, taxonomicStatus, species, genus, family, order1, class, phylum, kingdom)VALUES(:source, :taxonID, :acceptedNameUsageID, :taxonomicStatus, :species, :genus, :family, :order1, :class, :phylum, :kingdom)''', data)
    #db.commit()
    with open("taxa.txt", "r") as catalog_of_life:
        for line in catalog_of_life:
            line = line.split("\t")
            data = {"source": "catalog of life", "taxonID": line[0], "acceptedNameUsageID": line[4], "taxonomicStatus": line[6], "species": line[17] + " " + line[19], "genus": line[17].strip(), "family": line[15], "order1": line[13], "class": line[12], "phylum": line[11], "kingdom": line[10]}
            data = {x.decode('utf8'): v.decode('utf8') for x, v in data.items()}
            emptyCheck = check_empty_values(data)
            data = check_unknowns(data)

            if line[7] == "genus" and line[19].strip() not in genusSet and len(line[19].strip())>1:
                genusSet.add(line[19].strip())
                cursor.execute('''INSERT INTO gbif(source, taxonID, acceptedNameUsageID, taxonomicStatus, species, genus, family, order1, class, phylum, kingdom)VALUES(:source, :taxonID, :acceptedNameUsageID, :taxonomicStatus, :species, :genus, :family, :order1, :class, :phylum, :kingdom)''', data)

    db.commit()

def main():
    make_database()
    add_gbif_backbone_taxonomy()
    add_catalog_of_life_taxonomy()
    cursor.execute("CREATE INDEX index_gbif_species ON gbif (species);")
    cursor.execute("CREATE INDEX index_gbif_genus ON gbif (genus);")

if __name__ == "__main__":
    main()