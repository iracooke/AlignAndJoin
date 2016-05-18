#! /usr/bin/env python3

import argparse
import re
from subprocess import call

parser = argparse.ArgumentParser(description='Rearrange samples fasta into one fasta per locus')

parser.add_argument('infiles', type=argparse.FileType('r'),nargs='+')

args = parser.parse_args()
# print(args.accumulate(args.integers))


def read_fasta(fp):
    name, seq = None, []
    for line in fp:
        line = line.rstrip()
        if line.startswith(">"):
            if name: yield (name[1:], ''.join(seq))
            name, seq = line, []
        else:
            seq.append(line)
    if name: yield (name[1:], ''.join(seq))

# Read in all the sequences into memory
#

sequences = {} # Master dict of all sequences in all files

for fp in args.infiles:
    for locus_name, seq in read_fasta(fp):
        ns = sequences.get(locus_name,{})
        ns[fp.name] = seq
        sequences[locus_name] = ns

print('Read a total of '+str(len(sequences))+' sequences')


def build_fasta(loci_seqs,file_lengths):
    concat_seq = ''
    for name,length in file_lengths.items():
        # print(loci_seqs.get(name,'-'))
        concat_seq += loci_seqs.get(name,'-' * length)
        # print(concat_seq)
    return(concat_seq)


# Now for each sequence write its complete concatenated entry
#

call(['mkdir','-p',"aln"])

for name,sample_seqs in sequences.items():
    f = open("aln/"+name + '_alignable.fasta', 'w')
    for file_name,seq in sample_seqs.items():
        sample_name = re.match("(.*)_rename.fasta",file_name).group(1)
        f.write('>'+sample_name+'\n')
        f.write(seq+'\n')
    f.close()

