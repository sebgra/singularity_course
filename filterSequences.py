#! /usr/bin/env python3
# coding: utf-8
import sys
import argparse
import logging
import os
from Bio import SeqIO

"""
This script takes an input fasta file, and outputs a fasta file with sequences
1. whose length is > 28000 nt
2. having less than 5% N
Moreover it renames sequences : spaces are replaced with --
"""


def clean_name(name):
    return name.replace(" ", "--")


def main(args):
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="the path to the input file in fasta format",
    )
    arg_parser.add_argument(
        "-o", "--output", required=True, help="The path of the output file"
    )
    parsed_args = arg_parser.parse_args(args)

    logging.info(f"Input Fasta file : {parsed_args.input}")
    logging.info(f"Output Fasta file : {parsed_args.output}")

    with open(parsed_args.output, "w") as outfile:
        # We parse the fasta file again to remove sequences
        with open(parsed_args.input) as infile:
            for record in SeqIO.parse(infile, "fasta"):
                if (
                    len(record.seq) > 28000
                    and (
                        (record.seq.count("N") + record.seq.count("n"))
                        / len(record.seq)
                    )
                    < 0.05
                ):
                    print(f">{clean_name(record.description)}", file=outfile)
                    print(f"{record.seq}", file=outfile)


if __name__ == "__main__":
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    main(sys.argv[1:])
