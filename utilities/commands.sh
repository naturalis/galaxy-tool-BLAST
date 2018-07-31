wget http://rs.gbif.org/datasets/backbone/backbone-current.zip
unzip -j backbone-current.zip "Taxon.tsv"
python add_gbif_to_database.py
sh get_bold_taxonomy.sh
python add_bold_taxonomy.py
sudo wget ftp://ftp.ncbi.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.zip
unzip -j new_taxdump.zip "rankedlineage.dmp"
unzip -j new_taxdump.zip "merged.dmp"




#grep "accepted" Taxon.tsv > Taxon_accepted.tsv
#grep "species" Taxon_accepted.tsv > Taxon_species.tsv
#grep "genus" Taxon_accepted.tsv > Taxon_genus.tsv
#awk -F "\t" '{print $8"\t"$18"\t"$19"\t"$20"\t"$21"\t"$22"\t"$23}' Taxon_species.tsv > Taxon_species_filtered
#awk -F "\t" '{print $8"\t"$18"\t"$19"\t"$20"\t"$21"\t"$22"\t"$23}' Taxon_genus.tsv > Taxon_genus_filtered
#awk -F "\t" '{if($1 != "" && $2 != "" && $3 != "" && $4 != "" && $5 != "" && $6 != "" && $7 != ""){print $0}}' Taxon_species_filtered > Taxon_species_filtered_filtered
#awk -F "\t" '{if($1 != "" && $2 != "" && $3 != "" && $4 != "" && $5 != "" && $6 != "" && $7 != ""){print $0}}' Taxon_genus_filtered > Taxon_genus_filtered_filtered

