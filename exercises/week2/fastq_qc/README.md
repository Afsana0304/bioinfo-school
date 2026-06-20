# FASTQ QC mini-project

A small command-line tool that reads a FASTQ file, prints basic quality-control
(QC) statistics, and writes a single self-contained one-page HTML report with a
per-read mean-quality bar chart.

This was the Week 2 self-directed mini-project (FASTQ → QC stats + HTML report).

## Requirements

- **Python 3** (tested with the system `python3`).
- **No third-party packages** — `qc.py` and `make_example.py` use the Python
  standard library only, so there is nothing to `pip install`.

## Files

| File | Role |
|------|------|
| `qc.py` | The QC tool (input) |
| `make_example.py` | Regenerates the synthetic test data |
| `example.fastq` | Input: 20 synthetic reads (~50 bp each) |
| `qc_report.html` | Output: the generated HTML report |

## Inputs and outputs

- **Input:** a FASTQ file (standard 4-line-per-record format).
- **Outputs:**
  - a plain-text QC summary printed to the terminal, and
  - an HTML report file (`qc_report.html` by default).

The reported statistics are: number of reads, total bases, min / max / mean read
length, GC content (%), N bases (%), and mean Phred quality, plus a bar chart of
mean quality per read.

## How to run

From this directory (`exercises/week2/fastq_qc/`):

```bash
# Default: read example.fastq, write qc_report.html
python3 qc.py

# Custom input and output paths
python3 qc.py myreads.fastq myreport.html

# Regenerate the synthetic example.fastq (deterministic, fixed seed)
python3 make_example.py
```

Then open `qc_report.html` in a web browser to view the report.

## Assumptions and caveats

- Quality strings are assumed to use **Phred+33** encoding. Older Illumina data
  using Phred+64 would produce wrong quality numbers without any error being
  raised — a good example of agent-/tool-generated output that "runs" but is
  silently wrong.
- Records must be standard **4-line FASTQ** (header / sequence / `+` / quality).
  Malformed or truncated records raise a `ValueError`.
