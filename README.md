# galaxy-tool-BLAST
wrapper and scripts for blasting and finding taxonomy
## Getting Started
### Prerequisites
For now BLAST 2.6.0 is beeing used. Version 2.7.1 contains a bug and is unable to retrieve taxonomy information for tabular output.
To install BLAST the following commands are used.
```
cd /home/galaxy/Tools/
sudo wget ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.6.0/ncbi-blast-2.6.0+-x64-linux.tar.gz
sudo tar xvzf ncbi-blast-2.6.0+-x64-linux.tar.gz
sudo rm ncbi-blast-2.6.0+-x64-linux.tar.gz
sudo chmod 777 ncbi-blast-2.6.0+/bin/*
sudo ln -s /home/galaxy/Tools/ncbi-blast-2.6.0+/bin/blastn /usr/local/bin/blastn2.6.0
sudo ln -s /home/galaxy/Tools/ncbi-blast-2.6.0+/bin/makeblastdb /usr/local/bin/makeblastdb2.6.0
```
### Adding to galaxy<br />
```
cd /home/galaxy/Tools
sudo git clone https://github.com/naturalis/galaxy-tool-BLAST
sudo chmod 777 galaxy-tool-BLAST/*
sudo ln -s /home/galaxy/Tools/galaxy-tool-BLAST/blastn_wrapper.py /usr/local/bin/blastn_wrapper.py
sudo ln -s /home/galaxy/Tools/galaxy-tool-BLAST/blastn_add_taxonomy.py /usr/local/bin/blastn_add_taxonomy.py
sudo ln -s /home/galaxy/Tools/galaxy-tool-BLAST/blastn.sh /home/galaxy/galaxy/tools/identify/blastn.sh
sudo ln -s /home/galaxy/Tools/galaxy-tool-BLAST/blastn.xml /home/galaxy/galaxy/tools/identify/blastn.xml
```
Add the following line to /home/galaxy/galaxy/config/tool_conf.xml
```
<tool file="identify/cutadapt.xml" />
```
### Reference Taxonomy
To add the taxonomy to the blast results the scripts need a reference. Currently the taxonomy of BOLD, Genbank, GBIF and catalogue of life is being used. 
With the following commands references are downloaded, created and added to the server.
**BOLD**<br />
```
bash utilities/get_bold_taxonomy.sh
python add_bold_taxonomy.py
```
**GBIF and Catalogue of life**<br />
```
wget http://rs.gbif.org/datasets/backbone/backbone-current.zip
unzip -j backbone-current.zip "Taxon.tsv"
wget http://www.catalogueoflife.org/DCA_Export/zip-fixed/2018-07-31-archive-complete.zip
unzip -j 2018-07-31-archive-complete.zip "taxa.txt"
python add_gbif_to_database.py
```
**Genbank**<br />
```
sudo wget ftp://ftp.ncbi.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.zip
unzip -j new_taxdump.zip "rankedlineage.dmp"
unzip -j new_taxdump.zip "merged.dmp"
```
### Reference sequences
**BOLD**<br />
```

```
**Genbank**<br />
Genbank is big and always growing (https://www.ncbi.nlm.nih.gov/genbank/statistics/). Because of the amount of sequences it takes long to blast against this reference. A lot of times not all the sequences are needed. With the following commands you can make sub-selections of genbank.
```
wget ftp://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nt.gz
gunzip nt.gz
filter_nt.py
#download accessiontotaxon file
wget ftp://ftp.ncbi.nih.gov/pub/taxonomy/accession2taxid/nucl_gb.accession2taxid.gz
gunzip nucl_gb.accession2taxid.gz
#extract two columns
sed '1d' nucl_gb.accession2taxid | awk '{print $2" "$3}' > accession_taxonid
```
Now the selections are made, the fasta files need be indexed<br />
```
sudo makeblastdb2.6.0 -in CO1.fa -dbtype nucl -taxid_map accession_taxonid -parse_seqids
sudo makeblastdb2.6.0 -in 12S.fa -dbtype nucl -taxid_map accession_taxonid -parse_seqids
sudo makeblastdb2.6.0 -in ITS.fa -dbtype nucl -taxid_map accession_taxonid -parse_seqids
sudo makeblastdb2.6.0 -in 16S.fa -dbtype nucl -taxid_map accession_taxonid -parse_seqids
```


