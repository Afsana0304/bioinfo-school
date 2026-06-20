# Three ways an agent can use tools (Week 4, Exercise C)

**Task used as the example:** *"Given a list of UniProt IDs, return each
protein's length and organism."* (Same kind of task as `exercises/week3/
fetch_proteins.py`, which already pulls sequences from UniProt.)

The point of this exercise is not to build all three, but to notice that the
*same* task can be done in three very different ways — and each fails
differently.

## 1. Code mode — the agent writes a reusable script

- **What artifact do you get?** A script (e.g. `uniprot_table.py`) that takes a
  list of IDs and writes a table of length + organism. It lives in the repo, is
  version-controlled, and can be rerun by anyone.
- **What can silently go wrong?** Bugs that "run" but are wrong: parsing the
  wrong field, dropping IDs that 404 without warning, off-by-one length, or
  caching a stale result. The script looks authoritative even when a column is
  subtly incorrect.
- **When would I use it?** For a **reusable analysis** — anything I'll run more
  than once, share, or need to reproduce later.

## 2. Command mode — the agent runs commands / API calls directly

- **What artifact do you get?** Essentially none that persists — the agent runs
  `curl`/API calls in the terminal and reports the answer in chat. Fast, but the
  "how" disappears once the session ends.
- **What can silently go wrong?** No record of exactly what was queried, so the
  result is hard to reproduce or audit. Easy to copy a number out of a response
  by hand and transcribe it wrong, or to miss that the API returned a partial /
  rate-limited result.
- **When would I use it?** For **one-off exploration** — a quick "what's the
  length of P69905?" where I don't need to keep the workflow.

## 3. MCP / tool mode — the agent calls a typed tool

- **What artifact do you get?** A structured call to a defined tool (an MCP
  server or a function wrapper) with typed inputs and outputs. The interface is
  explicit, and the same tool can be reused across agents.
- **What can silently go wrong?** The tool can be a black box — if its internal
  logic is wrong (wrong database version, wrong field mapping) I may trust clean,
  typed output that is still incorrect. Setup and auth friction is also real.
- **When would I use it?** For a **production / repeated workflow** where I want a
  stable, well-defined interface that many agents or runs can rely on.

## Takeaway

Code mode gives me a reusable, reviewable artifact; command mode is fastest but
leaves no trail; MCP/tool mode gives a clean typed interface but hides its
internals. In every mode the same rule from this repo applies: **output that
looks clean is not automatically correct** — validate against what I expect
(here, e.g. organism = *Homo sapiens* and plausible lengths) before trusting it.
