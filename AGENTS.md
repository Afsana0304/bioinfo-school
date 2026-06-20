# AGENTS.md — working rules for this repo

Instructions for any AI agent working in this repository. These are project
rules, not generic advice — follow them before claiming a task is done.

- **Language / dependencies.** Use Python 3. Prefer the standard library; only
  add a third-party package (e.g. Biopython) when it genuinely simplifies the
  task, and say so. The mini-projects here run with no `pip install`.
- **Where things live.** Exercise data and scripts are under `exercises/week*/`.
  Course instructions are in `weeks/`. Don't scatter new files at the repo root.
- **Coordinate systems are the #1 trap.** GFF3/GTF coordinates are **1-based,
  inclusive**; Python slicing is **0-based, half-open**. A feature at GFF
  `start..end` maps to `seq[start-1:end]`. BED is 0-based half-open. State which
  convention you are using whenever you touch genomic positions.
- **Validate biology before claiming success.** Code that runs is not code that
  is correct. For any extracted/translated CDS, check: protein starts with **M**,
  ends with a stop (`*`), and nucleotide length is divisible by 3. Report these
  checks instead of assuming the output is right.
- **Be explicit about assumptions.** FASTQ quality is assumed Phred+33; flag it
  if data might be Phred+64. Call out genome build (GRCh37 vs GRCh38) and strand
  handling rather than guessing silently.
- **Don't commit generated or junk files.** No `.DS_Store`, no regenerated
  outputs (`qc_report.html`), no large model weights or data dumps.
- **Keep changes reviewable.** Small, focused commits. Don't rewrite working
  scripts unless asked; explain what you changed and why.
