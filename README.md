# Align and Concatenate Loci


A collection of scripts for aligning data at each locus separately and then concatenating into a single long alignment

## Requirements

- [mafft](http://mafft.cbrc.jp/alignment/software/) Required for aligning. If you want to use another aligner edit `align.sh`

- [infoalign](http://emboss.sourceforge.net/apps/release/6.6/emboss/apps/infoalign.html)  Required to remove poor alignments before concatenating

On OSX both mafft and infoalign can be installed with [homebrew](http://brew.sh/)

```bash
	brew tap homebrew/science
	brew install mafft
	brew install emboss
```

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


