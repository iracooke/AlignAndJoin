#! /usr/bin/env python3

import argparse
import os
import subprocess
import sys

parser = argparse.ArgumentParser(description='Concatenate aligned sequences')

parser.add_argument('--min-seqs',  metavar='minseqs', type=int,default=44)
parser.add_argument('--min-ident',  metavar='minident', type=float,default=0.9)

parser.add_argument('infiles',type=str,nargs='+')


args = parser.parse_args()

bindir,file = os.path.split(os.path.realpath(__file__))

os.environ['PATH'] = bindir


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
    op = subprocess.check_output(['aln_percentage.sh',fp.name])
    return(float(op.decode()))
    # return(call(['aln_percentage.sh',fp.name]))


def num_seqs(fp):
    op = subprocess.check_output(['/usr/bin/grep','-c',">",fp.name])
    return(int(op.decode()))
# Read in all the sequences into memory
#

sequences = {} # Master dict of all sequences in all files
files = {} # Lengths (should be fixed) of sequences in each file

for fn in args.infiles:

    fp = open(fn,'r')

    if ( (percent_identical(fp) < args.min_ident) or (num_seqs(fp) < args.min_seqs )):
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

