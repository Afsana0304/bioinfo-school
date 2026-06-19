#!/usr/bin/env python3
"""FASTQ quality-control summarizer (standard library only).

Reads a FASTQ file, computes basic QC statistics, prints them to the
terminal, and writes a single self-contained one-page HTML report
(qc_report.html) including a bar chart of mean quality per read.

Usage:
    python3 qc.py [input.fastq] [output.html]

Defaults: input=example.fastq, output=qc_report.html
"""

import html
import sys
from datetime import datetime


def parse_fastq(path):
    """Yield (name, sequence, quality) tuples from a 4-line-per-record FASTQ.

    Raises ValueError on malformed records (truncated file or mismatched
    sequence/quality lengths).
    """
    with open(path) as fh:
        while True:
            header = fh.readline()
            if header == "":          # clean end of file
                break
            seq = fh.readline()
            plus = fh.readline()
            qual = fh.readline()
            if not (header.startswith("@") and plus.startswith("+")):
                raise ValueError("Malformed FASTQ: expected @/+ marker lines")
            seq = seq.strip()
            qual = qual.strip()
            if len(seq) != len(qual):
                raise ValueError(
                    f"Seq/qual length mismatch in record {header.strip()!r}"
                )
            name = header[1:].split()[0]  # read id, sans '@' and comment
            yield name, seq, qual


def phred_scores(quality_string):
    """Convert a Phred+33 quality string into a list of integer scores."""
    return [ord(c) - 33 for c in quality_string]


def compute_stats(records):
    """Compute QC stats from an iterable of (name, seq, qual) records.

    Returns a dict of aggregate stats plus a per-read list (id + mean qual)
    used to draw the chart.
    """
    n_reads = 0
    lengths = []
    gc_count = 0
    n_count = 0
    total_bases = 0
    total_qual = 0          # sum of all per-base quality scores
    total_qual_bases = 0
    per_read = []           # [(read_id, mean_quality), ...]

    for name, seq, qual in records:
        n_reads += 1
        length = len(seq)
        lengths.append(length)
        total_bases += length

        upper = seq.upper()
        gc_count += upper.count("G") + upper.count("C")
        n_count += upper.count("N")

        scores = phred_scores(qual)
        total_qual += sum(scores)
        total_qual_bases += len(scores)
        read_mean_q = sum(scores) / len(scores) if scores else 0.0
        per_read.append((name, read_mean_q))

    if n_reads == 0:
        raise ValueError("No reads found in input file")

    return {
        "n_reads": n_reads,
        "min_len": min(lengths),
        "max_len": max(lengths),
        "mean_len": total_bases / n_reads,
        "total_bases": total_bases,
        "gc_content": 100 * gc_count / total_bases if total_bases else 0.0,
        "n_percent": 100 * n_count / total_bases if total_bases else 0.0,
        "mean_quality": total_qual / total_qual_bases if total_qual_bases else 0.0,
        "per_read": per_read,
    }


def render_quality_bars(per_read, width=720, bar_gap=2, max_q=40):
    """Return an inline SVG bar chart of mean quality per read."""
    n = len(per_read)
    plot_h = 220
    pad_left, pad_bottom, pad_top = 40, 40, 10
    bar_w = max(4, (width - pad_left) / n - bar_gap)

    bars = []
    for i, (name, mean_q) in enumerate(per_read):
        x = pad_left + i * (bar_w + bar_gap)
        h = (min(mean_q, max_q) / max_q) * plot_h
        y = pad_top + plot_h - h
        # Colour-code: green = good (>=30), amber = ok (>=20), red = poor.
        colour = "#2e8b57" if mean_q >= 30 else "#e0a800" if mean_q >= 20 else "#c0392b"
        title = html.escape(f"{name}: mean Q={mean_q:.1f}")
        bars.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{h:.1f}" '
            f'fill="{colour}"><title>{title}</title></rect>'
        )

    # Y-axis gridlines / labels at 0, 10, 20, 30, 40.
    grid = []
    for q in range(0, max_q + 1, 10):
        gy = pad_top + plot_h - (q / max_q) * plot_h
        grid.append(
            f'<line x1="{pad_left}" y1="{gy:.1f}" x2="{width}" y2="{gy:.1f}" '
            f'stroke="#eee" stroke-width="1"/>'
            f'<text x="{pad_left - 6}" y="{gy + 4:.1f}" text-anchor="end" '
            f'font-size="11" fill="#666">Q{q}</text>'
        )

    svg_h = pad_top + plot_h + pad_bottom
    return (
        f'<svg viewBox="0 0 {width} {svg_h}" width="100%" '
        f'font-family="sans-serif" role="img" '
        f'aria-label="Mean quality per read">'
        + "".join(grid)
        + "".join(bars)
        + f'<text x="{pad_left}" y="{svg_h - 12}" font-size="12" fill="#333">'
        f'Reads (left to right, in file order) — hover a bar for its value</text>'
        + "</svg>"
    )


def render_html(stats, source_path):
    """Build the full self-contained HTML report as a string."""
    chart = render_quality_bars(stats["per_read"])
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")

    rows = [
        ("Number of reads", f'{stats["n_reads"]:,}'),
        ("Total bases", f'{stats["total_bases"]:,}'),
        ("Min read length", f'{stats["min_len"]} bp'),
        ("Max read length", f'{stats["max_len"]} bp'),
        ("Mean read length", f'{stats["mean_len"]:.1f} bp'),
        ("GC content", f'{stats["gc_content"]:.2f} %'),
        ("N bases", f'{stats["n_percent"]:.2f} %'),
        ("Mean quality (Phred)", f'{stats["mean_quality"]:.2f}'),
    ]
    stat_rows = "".join(
        f"<tr><th>{html.escape(label)}</th><td>{html.escape(value)}</td></tr>"
        for label, value in rows
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>FASTQ QC Report</title>
<style>
  body {{ font-family: -apple-system, system-ui, sans-serif; color: #222;
         max-width: 820px; margin: 2rem auto; padding: 0 1rem; }}
  h1 {{ margin-bottom: 0.2rem; }}
  .meta {{ color: #777; font-size: 0.9rem; margin-bottom: 1.5rem; }}
  table {{ border-collapse: collapse; width: 100%; margin-bottom: 2rem; }}
  th, td {{ text-align: left; padding: 0.5rem 0.8rem; border-bottom: 1px solid #eee; }}
  th {{ width: 40%; color: #444; font-weight: 600; }}
  td {{ font-variant-numeric: tabular-nums; }}
  .card {{ border: 1px solid #e5e5e5; border-radius: 8px; padding: 1.2rem 1.5rem; }}
  .legend span {{ display: inline-block; margin-right: 1rem; font-size: 0.85rem; color: #555; }}
  .swatch {{ display: inline-block; width: 11px; height: 11px; border-radius: 2px;
            margin-right: 4px; vertical-align: middle; }}
</style>
</head>
<body>
  <h1>FASTQ Quality-Control Report</h1>
  <div class="meta">Source: <code>{html.escape(source_path)}</code> &middot; Generated {generated}</div>

  <div class="card">
    <table>{stat_rows}</table>

    <h2>Mean quality per read</h2>
    <div class="legend">
      <span><i class="swatch" style="background:#2e8b57"></i>Q &ge; 30 (good)</span>
      <span><i class="swatch" style="background:#e0a800"></i>Q 20&ndash;29 (ok)</span>
      <span><i class="swatch" style="background:#c0392b"></i>Q &lt; 20 (poor)</span>
    </div>
    {chart}
  </div>
</body>
</html>
"""


def main(argv):
    in_path = argv[1] if len(argv) > 1 else "example.fastq"
    out_path = argv[2] if len(argv) > 2 else "qc_report.html"

    stats = compute_stats(parse_fastq(in_path))

    # Print a plain-text summary to the terminal.
    print(f"QC summary for {in_path}")
    print(f"  Reads .............. {stats['n_reads']}")
    print(f"  Total bases ........ {stats['total_bases']}")
    print(f"  Read length ........ min {stats['min_len']}, "
          f"max {stats['max_len']}, mean {stats['mean_len']:.1f} bp")
    print(f"  GC content ......... {stats['gc_content']:.2f} %")
    print(f"  N bases ............ {stats['n_percent']:.2f} %")
    print(f"  Mean quality ....... {stats['mean_quality']:.2f} (Phred)")

    with open(out_path, "w") as fh:
        fh.write(render_html(stats, in_path))
    print(f"\nWrote HTML report to {out_path}")


if __name__ == "__main__":
    main(sys.argv)
