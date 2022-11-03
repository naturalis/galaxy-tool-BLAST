#!/bin/bash

outlocation=$(mktemp -d /data/files/XXXXXX)
SCRIPTDIR=$(dirname "$(readlink -f "$0")")

# sanity check
printf "Conda env: $CONDA_DEFAULT_ENV\n"
printf "Outlocation: $outlocation\n"
printf "Python version: $(python --version |  awk '{print $2}')\n"
printf "Biopython version: $(conda list | egrep biopython | awk '{print $2}')\n"
printf "Blastn version: $(blastn -version | head -n1 | awk '{print $2}')\n"
printf "Unzip version: $(unzip -v | head -n1 | awk '{print $2}')\n"
printf "Bash version: ${BASH_VERSION}\n"
printf "SCRIPTDIR: $SCRIPTDIR\n\n"

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
    $SCRIPTDIR"/blastn_add_taxonomy.py" -i $outlocation'/files/' -t /data/blast_databases/taxonomy/rankedlineage.dmp -m /data/blast_databases/taxonomy/merged.dmp -ts "${9}" -taxonomy_db /data/blast_databases/taxonomy/gbif_taxonmatcher
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
