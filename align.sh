#!/bin/bash

aln_dir="aln"

for f in `ls $aln_dir/*_alignable.fasta`;do
	bn=`basename $f`
	outname=${bn%_alignable.fasta}_aln.fasta
	echo $outname
	mafft-ginsi --ep 0.123 --quiet --thread 2 $f > $aln_dir/$outname
done


./bin/join_aln.py $aln_dir/*_aln.fasta > joined.fasta


