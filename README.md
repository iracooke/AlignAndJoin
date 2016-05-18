# Align and Concatenate Loci


A collection of scripts for aligning data at each locus separately and then concatenating into a single long alignment

Assuming that the starting data are fasta files containing sequences for each individual or sample.  Place these files into the current directory. Then run

```bash
	./bin/split_by_locus.py *.fasta
```

This will rearrange the data so that all sequences for each contig/locus are in a separate file.  These files will appear in the folder "aln" and should have the names like `Contig1_alignable.fasta`

Perform the actual alignment using mafft with the `align.sh` script

```bash
	./align.sh 
```

The joined alignment will appear in a file called `joined.fasta`

