from Bio import SeqIO
#its,  if "internal transcribed spacer" in str(record.description).lower() or "its" in str(record.description).lower() or "5.8" in str(record.description).lower():
#CO1, if "co1" in str(record.description.lower()) or "coi" in str(record.description.lower()) or "cox" in str(record.description.lower()) or "cytochrome c oxidase" in str(record.description.lower()) or "cytochrome oxidase" in str(record.description.lower()):
#12S, if "12S" in str(record.description).lower() or "mitochondrial" in str(record.description).lower():
#16S, if "16s" in str(record.description).lower() or "mitochondrial" in str(record.description).lower() or "mitochondrion" in str(record.description).lower():

with open("genbank.fa", "rU") as handle, open("CO1.fa",'a') as newfile:
    for record in SeqIO.parse(handle, "fasta"):
        if "co1" in str(record.description.lower()) or "coi" in str(record.description.lower()) or "cox" in str(record.description.lower()) or "cytochrome c oxidase" in str(record.description.lower()) or "cytochrome oxidase" in str(record.description.lower()) or "genome" in str(record.description.lower()):
            newfile.write(">"+str(record.description)+"\n")
            newfile.write(str(record.seq)+"\n")

with open("genbank.fa", "rU") as handle, open("ITS.fa",'a') as newfile:
    for record in SeqIO.parse(handle, "fasta"):
        if "internal transcribed spacer" in str(record.description).lower() or "its" in str(record.description).lower() or "5.8" in str(record.description).lower() or "genome" in str(record.description.lower()):
            newfile.write(">"+str(record.description)+"\n")
            newfile.write(str(record.seq)+"\n")

with open("genbank.fa", "rU") as handle, open("12S.fa",'a') as newfile:
    for record in SeqIO.parse(handle, "fasta"):
        if "12S" in str(record.description).lower() or "mitochondrial" in str(record.description).lower() or "genome" in str(record.description.lower()):
            newfile.write(">"+str(record.description)+"\n")
            newfile.write(str(record.seq)+"\n")

with open("genbank.fa", "rU") as handle, open("16S.fa",'a') as newfile:
    for record in SeqIO.parse(handle, "fasta"):
        if "16s" in str(record.description).lower() or "mitochondrial" in str(record.description).lower() or "mitochondrion" in str(record.description).lower() or "genome" in str(record.description.lower()):
            newfile.write(">"+str(record.description)+"\n")
            newfile.write(str(record.seq)+"\n")