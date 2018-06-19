def get_field_components_options(taxidlist):

    with open("/home/ubuntu/test.txt", "a") as testfile:
        testfile.write(taxidlist)

    options = [("hoi", "hoi", 2),("hallo", "hallo", 2)]
    if taxidlist != "none":
        options.append(("actino", taxidlist ,3))
    return options