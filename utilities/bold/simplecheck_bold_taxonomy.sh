for f in $1"/"*".tsv"
do
echo $f
echo $f"\n" >> $2
grep "Fatal error:" $f >> $2 || true
done
