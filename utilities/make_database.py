import sqlite3
db = sqlite3.connect('taxonomy_db')
cursor = db.cursor()
cursor.execute('''CREATE TABLE gbif(id INTEGER PRIMARY KEY, source TEXT, taxonID INTEGER, acceptedNameUsageID INTEGER, taxonomicStatus TEXT, species TEXT, genus TEXT, family TEXT, order1 TEXT, class TEXT, phylum TEXT, kingdom TEXT)''')
db.commit()
cursor.execute("CREATE INDEX index_gbif_species ON gbif (species);")
cursor.execute("CREATE INDEX index_gbif_genus ON gbif (genus);")
