#!/bin/bash
# Obtain a list of all the phyla located on BOLD
mkdir $1
for sp in $(wget -O - -q http://www.barcodinglife.org/index.php/TaxBrowser_Home | grep taxid | grep -o "[0-9]\">.* " | cut -f2 -d ">")
do
	# Use wget to download the file from the BoLD API and append it to the temporary fasta file
	echo $sp
	wget --waitretry=500 --read-timeout=200 --timeout=250 --continue -O - http://www.boldsystems.org/index.php/API_Public/sequence?taxon=$sp > $1"/"$sp"_sequences.fasta"
	echo "Sleep for 2 minutes" 
        sleep 2m
done

