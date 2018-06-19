#!/bin/bash
#location for production server
#outlocation=$(mktemp -d /media/GalaxyData/database/files/XXXXXX)
#location for the testserver
#outlocation=$(mktemp -d /media/GalaxyData/files/XXXXXX)
outlocation=$(mktemp -d /home/galaxy/ExtraRef/XXXXXX)
blastn_wrapper.py -it $1 -i $2 -db $3 -bt $4 -bm $5 -tl $6 -of $outlocation -outfmt $7

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

#rm -rf $outlocation
