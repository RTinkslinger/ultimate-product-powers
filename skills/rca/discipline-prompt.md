# RCA First-Pass Discipline Prompt

Loaded by `skills/rca/SKILL.md`. Invoked once per `/rca <target>` call, before the investigation loop.

## Step 0 — Query neutralization

The user's target may contain framing ("why did the stupid function break", "I think it's a race condition"). Produce a **neutralized query** that preserves semantic intent but strips:
- User's provisional diagnosis ("I think it's X")
- Emotional framing ("stupid", "broken")
- Leading questions ("why did X fail?" → "reproduction + failure mode of X")

Example:
- Target: "why is the login flow broken, I bet it's the JWT parsing"
- Neutralized: "reproduction + failure mode of the login flow; do not pre-assume JWT involvement"

## Step 1 — Hypothesis generation (N ≥ 3, contrastive)

Generate **at least 3** candidate causal hypotheses. Each must:
- Be a distinct causal mechanism, not a reformulation of the same cause.
- Pass the "consider the opposite" check — the list must include at least one hypothesis that *contradicts* the leading plausible cause.
- Not repeat the user's framing verbatim (that hypothesis can exist, but counts as one slot only).

If you can only think of 2, you have not tried hard enough. Force a third by asking: "What if the target itself is a symptom of something earlier in the chain?"

For each hypothesis:
- Claim (one sentence)
- Falsification criterion (one sentence — what specific observation would disprove this?)

## Step 2 — Evidence collection

Every hypothesis must have at least one evidence row supporting or refuting it. **Evidence = direct citation only.**

Valid evidence:
- Quote from a file currently in the repo, with `source: <path>:<line>`
- Quote from a log line, with `source: <log-path>:<timestamp>` or `:<line>`
- Quote from test output, with `source: test-run <test_selector>` where `<test_selector>` is the most specific identifier you have — pytest selector if available (`tests/test_x.py::test_foo`), full invocation command if not (`python3 tests/test_x.py`), or the test function name as a last resort. Include the exact output string in the `quote` column.
- Quote from git commit message, with `source: git <SHA>`
- Quote from a prior tool-call result in this session, with `source: session-tool-call <tool>`

Invalid evidence (reject):
- "In my experience, X usually causes Y" (no citation)
- "The function probably does Z" (speculation)
- "This implies that..." (inference without a quoted anchor)
- Paraphrased quotes (must be exact strings)

If an evidence quote cannot be grounded, do not add it. Flag the hypothesis as requiring investigation instead.

## Step 3 — Inconsistency matrix

Build the matrix: hypotheses as columns, evidence ids as rows. Fill each cell with `✓` (supports), `✗` (refutes), or `?` (irrelevant or unknown). A row with all `?` indicates the evidence is not usefully discriminating; consider removing it.

## Step 4 — Per-hypothesis confidence

For each hypothesis, assign `low | medium | high`:
- **high**: ≥ 2 supporting evidence rows AND no refuting evidence
- **medium**: ≥ 1 supporting evidence row AND no strong refuting evidence
- **low**: evidence is mixed, thin, or the hypothesis is exploratory

Not a numerical scale in v1. If you disagree with these thresholds for a specific case, note it in the reasoning.

## Step 5 — First-pass verdict

Name the leading hypothesis. Explain in one paragraph:
- Which evidence rows most strongly support it
- Which rows could still disprove it (falsification criterion)
- Why the alternatives are weaker given the evidence

If no hypothesis has ≥ medium confidence, the first pass is **not done** — proceed to the investigation loop (see `investigation-prompt.md`). Do not emit a weak verdict; go gather more evidence first.

## Output format

Write the result into sections §1-§2 of the canonical record (see `record-schema.md`). The investigation log (§3), judge pass (§4), resolution (§5), and references (§6) are populated by later stages.

## Hard rules (non-negotiable)

1. No hypothesis without a falsification criterion.
2. No evidence row without a resolvable citation.
3. No verdict claiming "high" confidence with fewer than 2 supporting evidence rows.
4. No paraphrased evidence — exact strings only.
5. If you cannot meet these rules for the given target, do not fake it — hand off to the investigation loop.
