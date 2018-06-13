#!/bin/bash
#location for production server
#outlocation=$(mktemp -d /media/GalaxyData/database/files/XXXXXX)
#location for the testserver
#outlocation=$(mktemp -d /media/GalaxyData/files/XXXXXX)
outlocation=$(mktemp -d /home/galaxy/ExtraRef/XXXXXX)
blastn_wrapper.py -it $1 -i $2 -db $3 -bt $4 -bm $5 -of $outlocation
mv -v $outlocation'/files/'*'.tabular' $6
mv $outlocation"/log.log" $7
echo $outlocation
#rm -rf $outlocation
