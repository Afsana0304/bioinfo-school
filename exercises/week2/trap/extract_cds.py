#!/usr/bin/env python3
"""Extract and translate CDS features from a genome + GFF3 annotation.

For each CDS in annotations.gff3 this prints:

    gene_name<TAB>nt_sequence<TAB>protein_sequence

Coordinate note: GFF3 uses 1-based, fully-closed coordinates (both the start
and end positions are included). Python string/Seq slicing is 0-based and
half-open. So a feature spanning GFF columns start..end maps to the slice
seq[start - 1 : end].
"""

from Bio import SeqIO
from Bio.Seq import Seq


def parse_attributes(field):
    """Parse a GFF3 attribute column (key=value;key=value) into a dict."""
    attrs = {}
    for pair in field.strip().split(";"):
        if not pair:
            continue
        key, _, value = pair.partition("=")
        attrs[key.strip()] = value.strip()
    return attrs


def load_genome(path):
    """Return {seq_id: Seq} for every record in a FASTA file."""
    return {rec.id: rec.seq for rec in SeqIO.parse(path, "fasta")}


def iter_cds(gff_path):
    """Yield (seqid, start, end, strand, attributes) for each CDS line."""
    with open(gff_path) as handle:
        for line in handle:
            if line.startswith("#") or not line.strip():
                continue
            cols = line.rstrip("\n").split("\t")
            if len(cols) < 9 or cols[2] != "CDS":
                continue
            seqid = cols[0]
            start = int(cols[3])  # 1-based, inclusive
            end = int(cols[4])    # 1-based, inclusive
            strand = cols[6]
            attrs = parse_attributes(cols[8])
            yield seqid, start, end, strand, attrs


def main(genome_path="genome.fa", gff_path="annotations.gff3"):
    genome = load_genome(genome_path)

    for seqid, start, end, strand, attrs in iter_cds(gff_path):
        chrom = genome[seqid]

        # 1-based inclusive (GFF3)  ->  0-based half-open (Python)
        nt = chrom[start - 1:end]
        if strand == "-":
            nt = nt.reverse_complement()

        protein = nt.translate(table=1)  # table 1 = standard genetic code

        gene_name = attrs.get("Name") or attrs.get("ID") or seqid
        print(f"{gene_name}\t{nt}\t{protein}")


if __name__ == "__main__":
    main()
