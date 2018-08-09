# Obtain a list of all the Kingdoms located on BOLD
for sp in $(wget -O - -q http://www.barcodinglife.org/index.php/TaxBrowser_Home | grep taxid | grep -o "[0-9]\">.* " | cut -f2 -d ">")
do
	# Use wget to download the file from the BoLD API and append it to the temporary fasta file
	echo $sp >> bold_log.txt
	wget --retry-connrefused --waitretry=400 --read-timeout=100 --timeout=150 -t 0 --continue -O $sp "http://www.boldsystems.org/index.php/API_Public/specimen?taxon=$sp&format=tsv" > species_info.tsv
        cat $sp >> bold_taxonomy.tsv
        rm $sp
	sleep 2m
done
