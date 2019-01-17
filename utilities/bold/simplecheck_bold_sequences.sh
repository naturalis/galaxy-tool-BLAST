#change "bold_fasta_files" to the folder where you have your bold fastafiles
for f in bold_fasta_files/*.fasta
do
echo $f
echo $f"\n" >> simplecheck_bold_sequences_log.txt
grep "<" $f >> simplecheck_bold_sequences_log.txt
done
