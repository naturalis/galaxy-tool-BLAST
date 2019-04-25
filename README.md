# galaxy-tool-BLAST
Wrapper for BLASTn, this repo can be used for the new (03-04-2019) galaxy 19.01 Naturalis server. The old galaxy 16.04 server is not supported anymore with this tool. This repo contains wrappers and scripts for blasting and finding taxonomy. See the wiki for some extra info about the reference databases https://github.com/naturalis/galaxy-tool-BLAST/wiki

## Getting Started
### Prerequisites
**BLAST 2.9.0+**<br />
```
cd /home/galaxy/Tools
wget https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.9.0+-x64-linux.tar.gz
tar xzvf ncbi-blast-2.9.0+-x64-linux.tar.gz
rm ncbi-blast-2.9.0+-x64-linux.tar.gz
chmod 777 ncbi-blast-2.9.0+/bin/*
```
Add the blast programs to /usr/local/bin for convenience
```
sudo ln -s /home/galaxy/Tools/ncbi-blast-2.9.0+/bin/makeblastdb /usr/local/bin/makeblastdb
sudo ln -s /home/galaxy/Tools/ncbi-blast-2.9.0+/bin/blastn /usr/local/bin/blastn

```
### Installing
Installing the tool for use in Galaxy
```
cd /home/galaxy/Tools
```
```
git clone https://github.com/naturalis/galaxy-tool-BLAST
```
```
chmod 777 galaxy-tool-BLAST/blastn_wrapper.py
```
Add the following line to /home/galaxy/galaxy/config/tool_conf.xml
```
<tool file="/home/galaxy/Tools/galaxy-tool-BLAST/blastn.xml" />
```
