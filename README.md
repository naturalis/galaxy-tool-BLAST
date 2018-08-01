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
```
