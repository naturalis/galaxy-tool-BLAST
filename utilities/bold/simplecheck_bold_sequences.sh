for f in $1"/"*".fasta"
do
echo $f
echo $f"\n" >> $2
grep "<" $f >> $2 || true
done
