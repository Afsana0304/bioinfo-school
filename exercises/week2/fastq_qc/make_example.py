#!/usr/bin/env python3
"""Generate a tiny synthetic example.fastq for QC testing.

Produces ~20 reads of ~50 bp in valid 4-line FASTQ format. Quality scores
use Phred+33 encoding and decline toward the 3' end (mimicking real Illumina
data), with occasional low-quality bases and a few N calls. Deterministic via
a fixed seed so the file is reproducible.
"""

import random

SEED = 2
N_READS = 20
READ_LEN = 50
BASES = "ACGT"


def make_sequence(length):
    """Random sequence; ~2% of positions become an ambiguous N base."""
    seq = []
    for _ in range(length):
        if random.random() < 0.02:
            seq.append("N")
        else:
            seq.append(random.choice(BASES))
    return "".join(seq)


def make_quality(length):
    """Phred+33 quality string that degrades toward the read's 3' end."""
    quals = []
    for i in range(length):
        # Mean quality drops linearly from ~38 to ~20 across the read.
        mean_q = 38 - (18 * i / length)
        q = int(random.gauss(mean_q, 3))
        q = max(2, min(40, q))          # clamp to a sane Phred range
        quals.append(chr(q + 33))       # Phred+33 encoding
    return "".join(quals)


def main(path="example.fastq"):
    random.seed(SEED)
    with open(path, "w") as fh:
        for i in range(1, N_READS + 1):
            # Slight length variation so min/max length stats are non-trivial.
            length = READ_LEN + random.randint(-3, 3)
            seq = make_sequence(length)
            qual = make_quality(length)
            fh.write(f"@read{i:03d} synthetic\n")
            fh.write(f"{seq}\n")
            fh.write("+\n")
            fh.write(f"{qual}\n")
    print(f"Wrote {N_READS} reads to {path}")


if __name__ == "__main__":
    main()
