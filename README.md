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

## Usage
