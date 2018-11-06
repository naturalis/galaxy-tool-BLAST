
class Genbank:
    def __init__(self, rankedlineage, merged):
        self.taxonomyDict = self.reference_taxonomy(rankedlineage)
        self.mergedTaxonDict = self.merged_taxonomy(merged)

    def reference_taxonomy(self, rankedlineage):
        taxonomyDict = {}
        with open(rankedlineage) as rankedlineage:
            for tax in rankedlineage:
                tax = tax.split("|")
                taxonid = tax[0]
                species = tax[1].strip() if tax[1].strip() else "unknown species"
                genus = tax[3].strip() if tax[3].strip() else "unknown genus"
                family = tax[4].strip() if tax[4].strip() else "unknown family"
                order = tax[5].strip() if tax[5].strip() else "unknown order"
                classe = tax[6].strip() if tax[6].strip() else "unknown class"
                phylum = tax[7].strip() if tax[7].strip() else "unknown phylum"
                kingdom = tax[8].strip() if tax[8].strip() else "unknown kingdom"
                superkingdom = tax[9].strip() if tax[9].strip() else "unknown superkingdom"
                taxonomyDict[str(tax[0].strip())] = {"species":species, "genus":genus, "family":family, "order":order, "class":classe, "phylum":phylum, "kingdom":kingdom,"superkingdom":superkingdom}
        return taxonomyDict

    def merged_taxonomy(self, merged):
        mergedDict = {}
        with open(merged) as merged:
            for taxid in merged:
                a = map(str.strip, taxid.split("|"))
                mergedDict[a[0]]=a[1]
        return mergedDict

    def check_merged_taxonomy(self, taxid, mergedTaxonDict):
        try:
            a = mergedTaxonDict[taxid]
            return a
        except:
            return "N/A"

    def find_genbank_taxonomy(self, hit):
        kingdom = "unknown kingdom"
        superkingdom = "unknown kingdom"
        taxid = hit.split("\t")[3]
        if taxid == "N/A":
            return hit.strip() + "\tGenbank\t" + "unknown kingdom / unknown phylum / unknown class / unknown order / unknown family / unknown genus / unknown species\n"
        else:
            taxonomydb = self.taxonomyDict
            try:
                kingdom = taxonomydb[taxid]["kingdom"]
                superkingdom = taxonomydb[taxid]["superkingdom"]
            except KeyError:
                mergedTaxid = self.check_merged_taxonomy(taxid, self.mergedTaxonDict)
                if mergedTaxid != "N/A":
                    taxid = mergedTaxid
                    kingdom = taxonomydb[mergedTaxid]["kingdom"]
                    superkingdom = taxonomydb[mergedTaxid]["superkingdom"]

            if kingdom and kingdom != "unknown kingdom":
                if taxonomydb[taxid]["kingdom"] == "Metazoa":
                    kingdomName = "Eukaryota"
                else:
                    kingdomName = taxonomydb[taxid]["kingdom"]
                return hit.strip() + "\tGenbank\t" + kingdomName + " / " + taxonomydb[taxid]["phylum"] + " / " + taxonomydb[taxid]["class"] + " / " + taxonomydb[taxid]["order"] + " / " + taxonomydb[taxid]["family"] + " / " + taxonomydb[taxid]["genus"] + " / " + taxonomydb[taxid]["species"] + "\n"
            elif superkingdom and superkingdom != "unknown superkingdom":
                return hit.strip() + "\tGenbank\t" + taxonomydb[taxid]["superkingdom"] + " / " + taxonomydb[taxid]["phylum"] + " / " + taxonomydb[taxid]["class"] + " / " + taxonomydb[taxid]["order"] + " / " + taxonomydb[taxid]["family"] + " / " + taxonomydb[taxid]["genus"] + " / " + taxonomydb[taxid]["species"] + "\n"
            else:
                return hit.strip() + "\tGenbank\t" + taxonomydb[taxid]["kingdom"] + " / " + taxonomydb[taxid]["phylum"] + " / " + taxonomydb[taxid]["class"] + " / " + taxonomydb[taxid]["order"] + " / " + taxonomydb[taxid]["family"] + " / " + taxonomydb[taxid]["genus"] + " / " + taxonomydb[taxid]["species"] + "\n"
