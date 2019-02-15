"""
"""
from Bio import SeqIO

def make_kingdom_dict():
    kingdomDict = {}
    with open("gbif_taxonomy.tsv","r") as gbif:
        for x in gbif:
            x = x.split("\t")
            if x[1] not in kingdomDict:
                kingdomDict[x[1]] = x[0]
            if x[2] not in kingdomDict:
                kingdomDict[x[2]] = x[0]
            if x[3] not in kingdomDict:
                kingdomDict[x[3]] = x[0]
            if x[4] not in kingdomDict:
                kingdomDict[x[4]] = x[0]
            if x[5] not in kingdomDict:
                kingdomDict[x[5]] = x[0]
    return kingdomDict

#>private_BOLD|NLFLM005-12|Potamogeton gramineus|Magnoliophyta|Liliopsida|Alismatales|Potamogetonaceae|Potamogeton|Potamogeton gramineus
def add_taxonomy(kingdomDict):
    with open("filtered_waterscan.fa", "r") as bold, open("filtered_waterscan_taxonomy.fa","a") as output:
        for record in SeqIO.parse(bold, "fasta"):
                description = str(record.description).split("|")
                if description[3] in kingdomDict:
                    kingdom = kingdomDict[description[3]]
                elif description[4] in kingdomDict:
                    kingdom = kingdomDict[description[4]]
                elif description[5] in kingdomDict:
                    kingdom = kingdomDict[description[5]]
                elif description[6] in kingdomDict:
                    kingdom = kingdomDict[description[6]]
                elif description[7] in kingdomDict:
                    kingdom = kingdomDict[description[7]]
                else:
                    print "no kingdom"
                    kingdom = "unknown kingdom"
                output.write(">"+description[0]+"|"+description[1]+"|"+description[2]+"|"+kingdom+"|"+description[3]+"|"+description[4]+"|"+description[5]+"|"+description[6]+"|"+description[7]+"|"+description[8]+"\n")
                output.write(str(record.seq)+"\n")


def main():
    kingdomDict = make_kingdom_dict()
    add_taxonomy(kingdomDict)

if __name__=="__main__":
    main()
