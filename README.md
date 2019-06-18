# galaxy-tool-BLAST
Wrapper for BLASTn, this repo contains wrappers and scripts for blasting and finding taxonomy. See the wiki for some extra info about the reference databases https://github.com/naturalis/galaxy-tool-BLAST/wiki. The scripts help to blast and find the associated taxonomy.

## Getting Started
### Prerequisites
**BLAST 2.8.1+**<br />
NOTE: This is not the newest blast+ version, but somehow version 2.9.0 gives an error when creating some blast reference databases.
```
cd /home/galaxy/Tools
wget https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.8.1/ncbi-blast-2.8.1+-x64-linux.tar.gz
tar xzvf ncbi-blast-2.8.1+-x64-linux.tar.gz
rm ncbi-blast-2.8.1+-x64-linux.tar.gz
chmod 777 ncbi-blast-2.8.1+/bin/*
```
Add the blast programs to /usr/local/bin for convenience
```
sudo ln -s /home/galaxy/Tools/ncbi-blast-2.8.1+/bin/makeblastdb /usr/local/bin/makeblastdb2.8.1
sudo ln -s /home/galaxy/Tools/ncbi-blast-2.8.1+/bin/blastn /usr/local/bin/blastn2.8.1
```
### Download
```
git clone https://github.com/naturalis/galaxy-tool-BLAST
```

## Usage (lite version)
All scripts are originally designed for the Naturalis infrastructure and galaxy server. If you want to use the scripts on your own hardware you need to use the "lite" version. To blast and get the final output with taxonomy takes two steps. First is the actual blasting, and after that adding the taxonomy. For this simple example we use a blast command, headerandcoverage_lite.py and blastn_add_taxonomy_lite.py. For a more advanced use or the for use in galaxy blasting will be done by the blastn_wrapper.py script.
<br />
**First let's blast:**<br />
```
blastn -query examplefasta/10seqs_example.fa -db nt -task megablast -num_threads 16 -max_hsps 1 -perc_identity 80 -out example_output -outfmt "6 qseqid stitle sacc staxid pident qcovs evalue bitscore" -max_target_seqs 10
```
**Add header and filter on coverage:**<br />
```
python headerandcoverage_lite.py -i example_output -cov 80
```
**Add taxonomy:**<br />
In this example we blasted against Genbank. To add taxonomy from this source we need the files rankedlineage.dmp and merged.dmp. The files can be downloaded from this page ftp://ftp.ncbi.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.zip. Make sure that the genbank sequence database is the same version as the taxonomy files. To add the genbank taxonomy execute the following command:
```
python blastn_add_taxonomy_lite.py -i lite_version/example_output_covfiltered.tabular -t lite_version/rankedlineage.dmp -m lite_version/merged.dmp -o taxonomy_example_output_covfiltered.tabular
```




