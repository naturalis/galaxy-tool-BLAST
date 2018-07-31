#!/bin/bash
#location for production server
#outlocation=$(mktemp -d /media/GalaxyData/database/files/XXXXXX)
#location for the testserver
#outlocation=$(mktemp -d /media/GalaxyData/files/XXXXXX)

outlocation=$(mktemp -d /home/galaxy/ExtraRef/XXXXXX)
blastn_wrapper.py -it $1 -i $2 -db $3 -bt $4 -bm $5 -of $outlocation -outfmt $6 -id "${10}"

#below the code for moving the files to the galaxy output, when no taxonomy need to be added
if [ $6 != "custom_taxonomy" ] || [ "${9}" == "none" ]
then
    if [ $1 == "zip" ]
    then
        zip -r -j $outlocation"/blast_output.zip" $outlocation'/files/'*'.tabular' --quiet
        mv $outlocation"/log.log" $7
        mv $outlocation"/blast_output.zip" $8
    fi
    if [ $1 == "fasta" ]
    then
        mv $outlocation"/log.log" $7
        mv $outlocation'/files/'*'.tabular' $8
    fi

#below the code to call the script to add taxonomy and move the files to the galaxy output
elif [ $6 == "custom_taxonomy" ] && [ "${9}" != "none" ]
then
    blastn_add_taxonomy.py -i $outlocation'/files/' -t /home/ubuntu/Marten/github_scripts/galaxy-tool-BLAST/utilities/rankedlineage.dmp -m /home/ubuntu/Marten/github_scripts/galaxy-tool-BLAST/utilities/merged.dmp -ts "${9}" -taxonomy_db /home/ubuntu/Marten/github_scripts/galaxy-tool-BLAST/utilities/taxonomy_db -bold_db /home/ubuntu/Marten/github_scripts/galaxy-tool-BLAST/utilities/bold_db
    if [ $1 == "zip" ]
    then
        zip -r -j $outlocation"/blast_output.zip" $outlocation'/files/'*taxonomy_*'.tabular' --quiet
        mv $outlocation"/log.log" $7
        mv $outlocation"/blast_output.zip" $8
    fi
    if [ $1 == "fasta" ]
    then
        mv $outlocation"/log.log" $7
        mv $outlocation'/files/'taxonomy_*'.tabular' $8
        if [ $9 == "GBIF" ]
        then
            mv $outlocation'/files/'orginaltaxonomy_*'.tabular' "${11}"
        fi
    fi
fi

rm -rf $outlocation
