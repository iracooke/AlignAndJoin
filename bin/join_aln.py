#! /usr/bin/env python3

import argparse
import os
import subprocess
import sys

parser = argparse.ArgumentParser(description='Concatenate aligned sequences')

parser.add_argument('infiles', type=argparse.FileType('r'),nargs='+')

args = parser.parse_args()
# print(args.accumulate(args.integers))

os.environ['PATH'] = '/Users/icooke/Projects/carla_loci/bin/'


def read_fasta(fp):
    name, seq = None, []
    for line in fp:
        line = line.rstrip()
        if line.startswith(">"):
            if name: yield (name, ''.join(seq))
            name, seq = line, []
        else:
            seq.append(line)
    if name: yield (name, ''.join(seq))


def percent_identical(fp):
    op = subprocess.run(['aln_percentage.sh',fp.name],check=True,stdout = subprocess.PIPE)
    return(float(op.stdout.decode()))
    # return(call(['aln_percentage.sh',fp.name]))


def num_seqs(fp):
    op = subprocess.run(['/usr/bin/grep','-c',">",fp.name],stdout = subprocess.PIPE)
    return(int(op.stdout.decode()))
# Read in all the sequences into memory
#

sequences = {} # Master dict of all sequences in all files
files = {} # Lengths (should be fixed) of sequences in each file


for fp in args.infiles:

    if ( (percent_identical(fp) < 0.9) or (num_seqs(fp) < 44 )):
        sys.stderr.write('Skipping alignment for '+fp.name+' '+  str(num_seqs(fp)) + '\n')
    else:
        fp_len = 0
        for name, seq in read_fasta(fp):
            if fp_len == 0:
                fp_len = len(seq)
                files[fp.name] = fp_len
            else:
                if (len(seq) != fp_len):
                    raise Error('All sequences in file must have the same length')
            ns = sequences.get(name,{})
            ns[fp.name] = seq
            sequences[name] = ns
    fp.close()

def build_fasta(loci_seqs,file_lengths):
    concat_seq = ''
    for name,length in file_lengths.items():
        # print(loci_seqs.get(name,'-'))
        concat_seq += loci_seqs.get(name,'-' * length)
        # print(concat_seq)
    return(concat_seq)


# Now for each sequence write its complete concatenated entry
#

for name,loci_seqs in sequences.items():
    # build_fasta(loci_seqs,files)
    print(name)
    print(build_fasta(loci_seqs,files))

