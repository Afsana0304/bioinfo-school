# Reflection — what I would and would not trust an agent with

I would trust an agent to do the work — write the scripts, fetch the data, run
the models — but I would not trust its results blindly. My rule after these four
weeks is *trust, but verify*. For anything an agent produces I will double-check
it: re-run it to see if I get the same result, and sanity-check the output
against what I actually expect rather than assuming it is right just because the
code ran. Week 2 made this concrete — the agent's CDS code ran cleanly and could
still have been silently wrong because of the 1-based vs 0-based coordinate trap,
and only my own biological checks (does the protein start with M, end in a stop,
have a length divisible by 3) would have caught it. Week 3 reinforced the same
habit: a low-confidence region in a structure prediction was not a failure but a
real, flexible part of the protein, which I only understood by looking past the
single score. So I will ask the agent *why* it got a result, not just *what* the
result is, every time. And instead of re-explaining my expectations in every
session, I will give the agent a guide up front (an `AGENTS.md` with my
conventions and the validation checks it must run) so it works the way I want by
default. In short: I trust an agent to accelerate the work, but I keep the role
of validating it against reality for myself.
