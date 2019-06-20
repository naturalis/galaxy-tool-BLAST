#!/bin/bash
outlocation=$(mktemp -d /home/galaxy/galaxy/database/XXXXXX)
SCRIPTDIR=$(dirname "$(readlink -f "$0")")

python $SCRIPTDIR"/blastn_wrapper.py" -it $1 -i $2 -db $3 -bt $4 -bm $5 -of $outlocation -outfmt $6 -cov "${10}" -id "${11}" -dbt "${13}"

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
    $SCRIPTDIR"/blastn_add_taxonomy.py" -i $outlocation'/files/' -t /media/Galaxydata/blastV2/rankedlineage.dmp -m /media/Galaxydata/blastV2/merged.dmp -ts "${9}" -taxonomy_db /home/galaxy/Tools/galaxy-tool-taxonmatcher/gbif_taxonmatcher
    if [ $1 == "zip" ]
    then
        zip -r -j $outlocation"/blast_output.zip" $outlocation'/files/'*taxonomy_*'.tabular' --quiet
        mv $outlocation"/log.log" $7
        mv $outlocation"/blast_output.zip" $8
    fi
    if [ $1 == "fasta" ]
    then
        mv $outlocation"/log.log" $7
        mv $outlocation'/files/'orginaltaxonomy_*'.tabular' "${8}"
        if [ $9 == "GBIF" ]
        then
            mv $outlocation'/files/'taxonomy_*'.tabular' "${12}"
        fi
    fi
fi
rm -rf $outlocation
