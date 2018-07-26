# Obtain a list of all the Kingdoms located on BOLD
for sp in $(wget -O - -q http://www.barcodinglife.org/index.php/TaxBrowser_Home | grep taxid | grep -o "[0-9]\">.* " | cut -f2 -d ">")
do
	# Use wget to download the file from the BoLD API and append it to the temporary fasta file
	echo $sp
	wget -O - "http://www.boldsystems.org/index.php/API_Public/specimen?taxon=$sp&format=tsv" > species_info.tsv
	sleep 1m
	cat species_info.tsv >> bold_taxonomy.tsv
done