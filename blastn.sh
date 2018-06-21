#!/bin/bash
#location for production server
#outlocation=$(mktemp -d /media/GalaxyData/database/files/XXXXXX)
#location for the testserver
#outlocation=$(mktemp -d /media/GalaxyData/files/XXXXXX)

outlocation=$(mktemp -d /home/galaxy/ExtraRef/XXXXXX)
blastn_wrapper.py -it $1 -i $2 -db $3 -bt $4 -bm $5 -tl $6 -of $outlocation -outfmt $7

#below the code for moving the files to the galaxy output, when no taxonomy need to be added
if [ $7 != "custom_taxonomy" ] || [ "${10}" == "none" ]
then
    if [ $1 == "zip" ]
    then
        zip -r -j $outlocation"/blast_output.zip" $outlocation'/files/'*'.tabular' --quiet
        mv $outlocation"/log.log" $8
        mv $outlocation"/blast_output.zip" $9
    fi
    if [ $1 == "fasta" ]
    then
        mv $outlocation"/log.log" $8
        mv $outlocation'/files/'*'.tabular' $9
    fi
fi
#below the code to call the script to add taxonomy and move the files to the galaxy output
if [ $7 == "custom_taxonomy" ] || [ "${10}" != "none" ]
then
    blastn_add_taxonomy.py -i $outlocation'/files/' -t /home/ubuntu/testmapMarten/test/Marten/github_scripts/galaxy-tool-BLAST/database/rankedlineage.dmp -m /home/ubuntu/testmapMarten/test/Marten/github_scripts/galaxy-tool-BLAST/database/merged.dmp -ts "${10}"
    if [ $1 == "zip" ]
    then
        zip -r -j $outlocation"/blast_output.zip" $outlocation'/files/'taxonomy_*'.tabular' --quiet
        mv $outlocation"/log.log" $8
        mv $outlocation"/blast_output.zip" $9
    fi
    if [ $1 == "fasta" ]
    then
        mv $outlocation"/log.log" $8
        mv $outlocation'/files/'taxonomy_*'.tabular' $9
    fi
fi













rm -rf $outlocation
