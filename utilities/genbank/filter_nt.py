from Bio import SeqIO
import threading
from threading import Thread
#awk -v RS='>' '{if (index(tolower($0), "co1") || index(tolower($0), "cox") || index(tolower($0), "cytochrome c oxidase")|| index(tolower($0), "cytochrome oxidase")) print ">"$0}' nt > awktest
def filter_co1():
    with open("nt", "rU") as handle, open("CO1.fa",'a') as newco1file:
        for record in SeqIO.parse(handle, "fasta"):
            if "co1" in str(record.description.lower()) or "coi" in str(record.description.lower()) or "cox" in str(record.description.lower()) or "cytochrome c oxidase" in str(record.description.lower()) or "cytochrome oxidase" in str(record.description.lower()):
                newco1file.write(">"+str(record.description)+"\n")
                newco1file.write(str(record.seq)+"\n")

def filter_its():
    with open("nt", "rU") as handle, open("ITS.fa",'a') as newitsfile:
        for record in SeqIO.parse(handle, "fasta"):
            if "internal transcribed spacer" in str(record.description).lower() or "its" in str(record.description).lower() or "5.8" in str(record.description).lower():
                newitsfile.write(">"+str(record.description)+"\n")
                newitsfile.write(str(record.seq)+"\n")

def filter_12s():
    with open("nt", "rU") as handle, open("12S.fa",'a') as new12sfile:
        for record in SeqIO.parse(handle, "fasta"):
            if "12S" in str(record.description).lower() or "mitochondrial" in str(record.description).lower():
                new12sfile.write(">"+str(record.description)+"\n")
                new12sfile.write(str(record.seq)+"\n")

def filter_16s():
    with open("nt", "rU") as handle, open("16S.fa",'a') as new16sfile:
        for record in SeqIO.parse(handle, "fasta"):
            if "16s" in str(record.description).lower() or "mitochondrial" in str(record.description).lower() or "mitochondrion" in str(record.description).lower():
                new16sfile.write(">"+str(record.description)+"\n")
                new16sfile.write(str(record.seq)+"\n")

def filter_matk():
    with open("nt", "rU") as handle, open("matk.fa", 'a') as newfile:
        for record in SeqIO.parse(handle, "fasta"):
            if ("chloroplast" in str(record.description.lower()) or
                        "matk" in str(record.description.lower()) or
                        "maturase" in str(record.description.lower()) or
                        "bac" in str(record.description.lower())):
                newfile.write(">" + str(record.description) + "\n")
                newfile.write(str(record.seq) + "\n")

def filter_rbcl():
    with open("nt", "rU") as handle, open("rbcl.fa", 'a') as newfile:
        for record in SeqIO.parse(handle, "fasta"):
            if ("ribulose-1,5-bisphosphate carboxylase/oxygenase" in str(record.description.lower()) or "rbcl" in str(record.description.lower()) or "chloroplast" in str(record.description.lower()) or "plastid" in str(record.description.lower())):
                newfile.write(">" + str(record.description) + "\n")
                newfile.write(str(record.seq) + "\n")

if __name__ == '__main__':
    Thread(target = filter_co1).start()
    Thread(target = filter_its).start()
    Thread(target=filter_12s).start()
    Thread(target=filter_16s).start()
    Thread(target=filter_matk).start()
