#! /usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description='Check lengths within a fasta file are all the same')

parser.add_argument('fasta_file', type=argparse.FileType())

args = parser.parse_args()
# print(args.accumulate(args.integers))


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

with args.fasta_file as fp:
    for name, seq in read_fasta(fp):
        print(len(seq))