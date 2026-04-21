# RCA Investigation Loop Prompt

Loaded by `skills/rca/SKILL.md`. Invoked after first-pass when any of:
- Fewer than 3 hypotheses have ≥ 1 grounded evidence citation.
- Inconsistency matrix has > 50% `?` cells.
- No hypothesis has a falsification criterion grounded in available data.

## Loop contract

```
while (not converged) AND (rounds < 10):
  1. Identify unfilled evidence slots from the canonical record
  2. Prioritize gaps that most constrain the leading hypothesis
  3. Dispatch read-only tool calls (small batch, 3-5 per round)
  4. Append new evidence rows to the record
  5. Re-evaluate the inconsistency matrix
  6. Check convergence

if converged → proceed to judge pass
if rounds capped without convergence → status=abstained, skip judges, emit gap report
if hypothesis space narrowed to ≤ 1 surviving → proceed to judge pass with annotation
```

## Tool scope

### Allowed

- `Read` — any file in the repo or user-pointed path
- `Grep`, `Glob` — search the repo
- `Bash` — pure queries only:
  - `ls`, `cat`, `head`, `tail`, `file`, `wc`
  - `git log`, `git diff`, `git blame`, `git show`, `git status`
  - Read-only database queries (`SELECT` only; no `INSERT`/`UPDATE`/`DELETE`/`DROP`)
- `Bash` — running **existing** test commands:
  - Examples: `pytest path/to/failing_test.py -v`, `npm test -- --run path/to/test.spec.ts`
  - Allowed because these invoke tests already defined in the repo; we observe their behavior.
  - **Excludes** test commands with side effects:
    - Snapshot-updating commands (`--update-snapshots`, `-u`, etc.)
    - Anything writing fixtures, DB state, or generated files
    - Anything containing `--write`, `--update`, `--save`, `--commit`
  - Inspect the command text before running. Decline if side effects are apparent.

### Explicitly disallowed

- `Write`, `Edit`, `NotebookEdit` — no file mutation under any circumstance.
- `Bash` — destructive or mutating commands:
  - `rm` (any variant), `rmdir`, `mv`, `cp` (with overwrite)
  - `git reset --hard`, `git push`, `git commit`, `git clean -f`, `git checkout --`, `git rebase`
  - `terraform apply`, `terraform destroy`, DB mutations, package installs
  - Any command with `--force`, `-f`, `-y`, `--yes`
- Creating or modifying git commits, branches, PRs, tags.
- Modifying existing `.rca/` records (append to current-record only; past records are immutable).

If a tool call violates these rules, do not issue it. Record the gap as unresolvable instead.

## What each round does

1. **Identify gaps.** Look at the canonical record's §2 evidence table and inconsistency matrix. A gap is: a hypothesis row in the matrix with all `?`, OR a hypothesis with fewer than 1 `✓` cell, OR a claim in a hypothesis that lacks a supporting evidence row.

2. **Prioritize.** Focus on gaps that would most change the verdict:
   - Missing evidence on the leading hypothesis (would strengthen or falsify the main verdict)
   - Missing evidence on a counter-hypothesis (would confirm or rule out an alternative)

3. **Dispatch tools.** Small batch (3-5 tool calls). Examples per target type:
   - Target is a failing test → `Read` the test file, `Grep` for the function under test, `git blame` that function, `git log` for recent changes near it
   - Target is an error message → `Grep` for the literal error string across the repo, `Read` files that emit it
   - Target is a commit → `git show <SHA>`, `Read` each changed file, `Grep` for call sites
   - Target is a log excerpt → `Read` the log, `Grep` for timestamps around the error

4. **Append evidence.** Each new evidence row must cite a specific `source: <path>:<line>` or similar. Paraphrasing forbidden.

5. **Re-evaluate matrix.** Update `✓`/`✗`/`?` cells as new evidence arrives.

6. **Check convergence** (see below).

## Convergence check

Converged if **any** of:
- A round yielded no new evidence AND ≥ 3 hypotheses have `high` or `medium` confidence.
- The inconsistency matrix has ≤ 20% `?` cells AND one hypothesis has strictly more `✓` cells than all others.
- Hypothesis space narrowed to 1 surviving (all others have ≥ 1 strong `✗` and no `✓`).

**Hypothesis space exhausted** (special case, not convergence): if investigation rules out all first-pass hypotheses (every first-pass H has ≥ 1 strong `✗` and 0 `✓`), annotate "first-pass hypothesis space exhausted; rely on judge pass for new candidates" in §3 and proceed to judge pass. Judges will propose their own hypotheses in their fresh-pass.

## Exit conditions

| Condition | Record state |
|---|---|
| Converged in ≤ 10 rounds | status = resolved (or pending judge verdict); proceed to judge pass |
| Hypothesis space narrowed to 1 | status = resolved (pending judge); proceed to judge pass |
| Hypothesis space exhausted | status = pending judge pass; proceed with annotation |
| Hit 10-round cap without convergence | status = abstained; skip judges; emit gap report in §5 |

## Abstention output format

When abstaining after max rounds, §5 Resolution must contain:
- Canonical verdict: `abstain`
- Canonical source: `first-pass-unchallenged` (no judges ran)
- Abstain gaps: enumerated list of what additional evidence would resolve the verdict (e.g., "runtime trace of function X under input Y", "commit preceding SHA Z that introduced the regression", "logs from environment E not currently in repo")
- Causal chain: partial — list the evidence gathered and the contradictions found

The skill does not pretend to have an answer. It reports what it has, what's missing, and what would unblock.
