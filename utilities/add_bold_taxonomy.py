"""

"""
import sqlite3
db = sqlite3.connect('bold_db')


def make_database():
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE bold(id INTEGER PRIMARY KEY, source TEXT, processid TEXT, species TEXT, genus TEXT, family TEXT, order1 TEXT, class TEXT, phylum TEXT, kingdom TEXT)''')
    db.commit()
    cursor.execute("CREATE INDEX index_bold_processid ON bold (processid);")

def check_empty_values(data):
    a = 0
    for taxon in data:
        a += 2 if not data["processid"] else 0
        a += 1 if not data["species"] else 0
        a += 1 if not data["genus"] else 0
        a += 1 if not data["family"] else 0
        a += 1 if not data["order1"] else 0
        a += 1 if not data["class"] else 0
        a += 1 if not data["phylum"] else 0
    if a >= 2:
        #print data
        #print a
        return False

    else:
        return True

def check_unknowns(data):
    for x in data:
        if not data[str(x)]:
            data[str(x)] = "unknown "+str(x)
    return data

def add_bold_taxonomy():
    cursor = db.cursor()
    with open("bold_taxonomy.tsv", "r") as bold:
        for line in bold:
            line = line.split("\t")
            data = {"source":"bold", "processid":line[0], "species":line[21], "genus":line[19].strip(), "family":line[15], "order1":line[13], "class":line[11], "phylum":line[9], "kingdom":"unknown kingdom"}
            data = {x.decode('utf8'): v.decode('utf8') for x, v in data.items()}
            #emptyCheck = check_empty_values(data)
            data = check_unknowns(data)
            #if emptyCheck:
            cursor.execute('''INSERT INTO bold(source, processid, species, genus, family, order1, class, phylum, kingdom)VALUES(:source, :processid, :species, :genus, :family, :order1, :class, :phylum, :kingdom)''', data)
    db.commit()
def main():
    make_database()
    add_bold_taxonomy()

if __name__ == "__main__":
    main()