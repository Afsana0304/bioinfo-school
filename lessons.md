# lessons.md — your prep log

One file for the whole prep. Keep two kinds of entry in **separate subsections each week** — don't mix them in one paragraph.

| Subsection | What goes here | How much detail |
|------------|----------------|-----------------|
| **From the materials** | Notes while watching or reading; answers to each week's reflection exercises | Usually one sentence per video chunk or paper section; reflection exercises can be a short paragraph each |
| **Surprises** | Moments an LLM or agent surprised you — good or bad — in chat or in the IDE | Concrete: tool/model, what you asked, what came back, optional takeaway |

Commit and push weekly. By week 4 this file is one of the most useful artifacts you bring to Brno. (`reflection.md` in week 4 is separate — one final paragraph for assessment.)

---

## From the materials — what to write

While watching or reading, stop every ~20 minutes (or after each major section) and add a line answering:

- *Video:* **What's the one thing I'd want to test from what I just heard?**
- *Paper:* **What claim would I most want to verify on my own data?**

Each week may also assign a **reflection exercise** (structured thinking using the week's mental model). Put those answers here too — they are not required to be personal chat logs.

---

## Surprises — what to write

Add an entry whenever an LLM or agent catches you off guard. Include enough detail that you (or a classmate) could understand the moment months later.

- **When** — approximate date
- **Tool / model** — e.g. ChatGPT (free), Claude, Antigravity agent, Cursor, …
- **What you asked** — paste or paraphrase the prompt; name any file or data involved
- **What happened** — the surprising part
- **Takeaway** (optional) — one line on what you'd do differently

**Bad (too vague):** *"ChatGPT hallucinated something."*

**Good:**

> **2026-05-26 · ChatGPT (free, no browsing)** — Asked: *"What is the Ensembl ID for human BRCA1?"* Answered confidently with `ENSG00000012048` — correct — then cited a made-up paper (*Smith et al., Nature 2019*) and a DOI that 404s. **Takeaway:** right gene, invented provenance; never trust citations without checking.

> **2026-06-03 · Antigravity agent** — Asked it to filter a BED file to chr21. Code ran, printed 1,842 lines, looked plausible. Checked: 0-based coordinates on a file the header said was 1-based. **Takeaway:** spot-check coordinate conventions before trusting counts.

---

## Your entries

(Add below. Newest at the bottom is fine — stay consistent.)

### Week 1

#### From the materials

<!-- Karpathy / GeneGPT notes; reflection exercise (three tasks, why hard or easy for an LLM) -->

#### Surprises

<!-- Chatbot exercise; anything else that caught you off guard -->

### Week 2

#### From the materials

<!-- ReAct / Karpathy Software 3.0 notes; trap-exercise discussion questions -->

#### Surprises

<!-- Trap exercise, mini-project, agent moments — be specific -->

2026-06-19 · Claude Code (2.1, Pro subscription) — Asked it to read genome.fa and annotations.gff3, extract each CDS, translate to protein, and print gene_name<TAB>nt_sequence<TAB>protein_sequence (the Week 2 trap prompt, given with no hints about coordinate systems). I expected it to fall into the 1-based GFF3 vs 0-based Python trap. It didn't — it applied seq[start-1:end] on its own and returned correct proteins: alpha_orf → MKFGQF*, beta_orf → MAAPKL*. I verified by hand: both start with M, end with * (stop), and are 21 nt (divisible by 3). Takeaway: the script ran without errors, but that alone didn't prove it was right — my own biology checks did. I need to keep verifying agent output against domain rules rather than trusting that it ran.

### Week 3

#### From the materials

<!-- Jumper lecture / CARBON reading notes -->

#### Surprises

2026-06-19 · ColabFold (AlphaFold2) + ESM2 (Colab) — Folded human ubiquitin (76 aa) in ColabFold and embedded 45 proteins with ESM2 (esm2_t6_8M). Surprise: I expected the low-confidence (non-blue) region on the ubiquitin structure to mean the model got that part wrong. It was the C-terminal tail, which is genuinely flexible in real life — so the low pLDDT there was the model being *correct* about uncertainty, not making a mistake. Low confidence ≠ error. On the embedding side, ESM2 was never told the family labels, yet the UMAP still separated kinases, GPCRs, immunoglobulins and oxygen-binding proteins into clean groups. Takeaway / validation hook: don't trust a single overall score or a nice picture — look at the confidence signal (pLDDT colouring on a structure, family colouring on an embedding plot) and check it matches what I'd expect.

### Week 4

#### From the materials

<!-- MCP / BixBench notes -->

#### Surprises

2026-06-20 · Claude Code (Opus, used to package my repo for week 4) — I had the agent write up my week 3 results into results.md from my screenshots. In the embeddings section it stated that I had "performed a validation check" by colouring the UMAP by family. I hadn't done any separate validation step — colouring by family was just part of the plot, so the agent had overstated what I actually did. I caught it and asked why it wrote that, and it corrected the wording. Takeaway: an agent can quietly overclaim or invent steps even when it is only *documenting* my own work, not just when it writes code. The week 2 lesson (verify agent output against reality) applies to the prose and write-ups too, not only to results — read what the agent says you did and make sure it is true.
