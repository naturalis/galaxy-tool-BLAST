"""
def taxon_filter(database):
    options = [("None","none", 1)]
    database = [i.encode('utf-8') for i in database]
    for x in database:
        if "v5" not in str(x).lower():
            options = [("None","none", 1)]
            break
        else:
            options.append(("Actinopterygii", "/home/ubuntu/testmapMarten/test/Marten/github_scripts/galaxy-tool-BLAST/database/Actinopterygii_taxidlist",1))
    return options

def taxonomy_source_list(database):
    options = [("None","none", 1)]
    options_dict = {}
    options_dict["NCBI"] = ("NCBI", "NCBI", 1)
    options_dict["BOLD"] = ("BOLD", "BOLD", 1)
    options_dict["GBIF"] = ("GBIF", "GBIF", 1)
    options_dict["default"] = ("Original taxonomy of the database", "default", 1)
    mem = []
    database = [i.encode('utf-8') for i in database]
    for x in database:
        if "v5" in str(x).lower():
            mem.append("NCBI")
        if "bold" in str(x).lower():
            mem.append("BOLD")

    if "NCBI" in mem and "BOLD" in mem:
        options_dict.pop("NCBI")
        options_dict.pop("BOLD")
    elif "NCBI" in mem and "BOLD" not in mem:
        options_dict.pop("BOLD")
    elif "NCBI" not in mem and "BOLD" in mem:
        options_dict.pop("NCBI")

    for y in options_dict:
        options.append(options_dict[y])

    return options

"""