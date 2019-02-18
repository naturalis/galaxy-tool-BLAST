#change "bold_taxonomy_files" to the folder where you have your bold taxonomy files
for f in bold_taxonomy_files/*.tsv
do
echo $f
echo $f"\n" >> simplecheck_bold_taxonomy_log.txt
grep "Fatal error:" $f >> simplecheck_bold_taxonomy_log.txt || true
done
