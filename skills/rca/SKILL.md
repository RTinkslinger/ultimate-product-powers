---
name: rca
description: Use when the user types /rca <target> to produce a disciplined root-cause analysis on any pointed-at target — a bug, failing test, file, error, commit, or prior diagnosis. Performs strict ACH reasoning with citation-only evidence, runs a read-only investigation loop, dispatches 3 parallel fresh-context judges (skeptic, evidence-auditor, safety-evaluator), conditionally fires a tiebreaker on disagreement, and writes a canonical hypothesis record to .rca/. Advisory-only — never modifies repo state, never applies a fix.
---

# /rca — Disciplined Root-Cause Analysis

## Overview

The user has invoked `/rca <target>`. Your job is to produce a grounded, evidence-cited RCA on the target with no assumption-based claims.

**Quality bar (non-negotiable):**
- No hypothesis without a direct-citation evidence row.
- No evidence without a resolvable source quote (string-matchable).
- No verdict the judges haven't reviewed (unless investigation abstained).
- Never modify repo state. This skill is advisory-only.

## When to use

- User explicitly types `/rca <target>` where `<target>` is any reference (path, description, failing test, commit, error, URL to a log, prior RCA record).
- Not auto-triggered. Not invoked from other skills in v1.

## The 8-stage flow

### Stage 0 — Intake

Parse the target. Determine `target_type`:
- `path` if target resolves to a file in the repo.
- `test` if target is a test name or pytest-style selector (`path/to/test.py::test_foo`).
- `commit` if target is a git SHA.
- `log` if target is a log path or quoted log excerpt.
- `description` if target is prose ("the login is broken", "why does X fail").
- `other` otherwise.

**Ambiguity check.** If target is too vague to pin down (e.g., `"the bug"`, `"the test"`, `"yesterday's error"` without specifics), do NOT proceed with a guess. Run a read-only survey:
- Recent failing tests (`git log --oneline -20`, `find . -name "*.fail" -o -name "*error*"`, check CI artifacts).
- Files modified in last 10 commits (`git log --name-only -10`).
- Error files sitting in the repo (grep for `ERROR|FAIL|Exception` in logs).

Surface 2-5 candidates with one-line context each:

```
/rca "the bug" is ambiguous. Candidates:
1. tests/test_auth.py::test_login_redirect — failing as of commit abc1234 (3 hours ago)
2. logs/2026-04-21-api.log — "ValueError: bad token" at 14:03
3. src/parser.py — modified in commit def5678 (yesterday), no test coverage added
4. .github/workflows/ci.yml — failing since commit 9012345
Please pick 1-4, or pass a more specific target.
```

Wait for user reply. Do NOT proceed with a default choice.

**Invalid target.** If target looks like a path but the file doesn't exist, reply: `Target <target> not found. Did you mean <closest-match>? Please specify a valid path, test selector, commit SHA, or description.`

### Stage 1 — Query neutralization (G2)

Load `discipline-prompt.md` Step 0. Produce the neutralized query. This is the first section of the canonical record.

### Stage 2 — First-pass ACH discipline

Follow `discipline-prompt.md` Steps 1-5:
- Generate ≥ 3 hypotheses with contrastive-CoT (include one that contradicts the most plausible).
- Every hypothesis gets a falsification criterion.
- Every hypothesis needs ≥ 1 evidence row with a resolvable citation.
- Build the inconsistency matrix.
- Per-hypothesis confidence: low | medium | high.
- Emit first-pass verdict — or mark as unfinished if no hypothesis has ≥ medium confidence.

Do not fabricate evidence. If you cannot cite something, do not cite it. Let the investigation loop fill the gap.

### Stage 3 — Investigation loop (if needed)

If the first pass has any of:
- The number of hypotheses with ≥ 1 citation is less than 3 (i.e., 0, 1, or 2 hypotheses are grounded).
- More than 50% of inconsistency-matrix cells are `?`.
- No hypothesis has a data-grounded falsification criterion.

Then enter the investigation loop. Follow `investigation-prompt.md`:
- Read-only + safe-side-effect tools only (Read, Grep, Glob, Bash queries, existing-test runs).
- **Never** use Write, Edit, destructive Bash.
- Each round: identify gaps → prioritize → dispatch 3-5 tool calls → append evidence → re-evaluate matrix → check convergence.
- Hard cap: 10 rounds. If not converged by round 10, status = `abstained`, skip judges, emit gap report.

### Stage 4 — Judge dispatch (PARALLEL)

If the investigation converged (or was not needed), dispatch 3 Agent-tool calls **in a single message** (parallel execution) to the `rca-judge` agent.

**Subagent-type fallback:** if `rca-judge` is not in the available `subagent_type` list (e.g., the skill was just installed and hasn't been picked up yet), use `general-purpose` and paste the full content of `~/.claude/skills/rca/judge-roles/<role>.md` into the dispatch prompt before the role-specific inputs. The judge prompt is self-contained.

```
Call 1:
  subagent_type: rca-judge
  description: "Skeptic review of /rca record"
  prompt: |
    ROLE: skeptic

    TARGET: <user's verbatim target>
    NEUTRALIZED: <neutralized query>

    FIRST-PASS RECORD:
    <paste §1-§3 of the canonical record in full>

    CITED ARTIFACTS:
    <paste only the file excerpts / log lines / test output that are quoted in the evidence table, with source labels>

    INVESTIGATION LOG SUMMARY:
    <rounds taken, stop reason, tools-dispatched count>

    Produce the output in the exact format specified in skills/rca/judge-roles/skeptic.md.

Call 2:
  subagent_type: rca-judge
  description: "Evidence-auditor review of /rca record"
  prompt: |
    ROLE: evidence-auditor
    <same inputs as Call 1>
    Produce output per skills/rca/judge-roles/evidence-auditor.md.

Call 3:
  subagent_type: rca-judge
  description: "Safety-evaluator review of /rca record"
  prompt: |
    ROLE: safety-evaluator
    <same inputs as Call 1>
    Produce output per skills/rca/judge-roles/safety-evaluator.md.
```

Wait for all 3 responses.

### Stage 5 — Disagreement check

Trigger tiebreaker if **any** of:
- `final_verdict` values across the 3 judges are not unanimous.
- Any judge emitted `critical` flag.
- First-pass verdict disagrees with majority-of-3 final_verdict.

### Stage 6 — Tiebreaker (conditional)

If disagreement fired, dispatch the 4th Agent-tool call:

```
Call 4:
  subagent_type: rca-judge
  description: "Tiebreaker on /rca judge disagreement"
  prompt: |
    ROLE: tiebreaker

    <same target / neutralized / first-pass-record / cited-artifacts / investigation-log inputs>

    JUDGE 1 (skeptic) OUTPUT:
    <paste Call 1 output in full>

    JUDGE 2 (evidence-auditor) OUTPUT:
    <paste Call 2 output in full>

    JUDGE 3 (safety-evaluator) OUTPUT:
    <paste Call 3 output in full>

    DISAGREEMENT REASON: <which trigger fired>

    Produce output per skills/rca/judge-roles/tiebreaker.md.
```

### Stage 7 — Resolve verdict

```
if tiebreaker_ran:
    canonical_verdict = tiebreaker.final_verdict
    canonical_source = "tiebreaker"
elif three_judges_ran:
    canonical_verdict = majority([j.final_verdict for j in judges])
    canonical_source = "majority-3"
else:  # investigation abstained before judge pass
    canonical_verdict = first_pass.verdict
    canonical_source = "first-pass-unchallenged"
    status = "abstained"
```

### Stage 8 — Write outputs

1. **Ensure `.rca/` exists.** If not, create the directory and write `.rca/.gitignore` with a single line of content: `telemetry/`. (That ignores the `telemetry/` subdirectory but keeps record `.md` files trackable; the user can tighten the ignore later if they prefer to keep records out of git too.)

2. **Write canonical record.** Path: `.rca/<ISO-timestamp>-<slug>.md`. Slug = kebab-case of neutralized query's first 6 words, max 40 chars. Fill in every section per `record-schema.md`.

3. **Write telemetry.** Path: `.rca/telemetry/<ISO-timestamp>.jsonl`. One JSON object per line, one line per stage event. **Every line must include `rca_id` and `event`** (`target` and `created` are required only on the first-pass event; subsequent events inherit by `rca_id`):
   - First-pass: `{"rca_id": "...", "target": "...", "created": "...", "event": "first-pass", "data": {"hypotheses": [...], "evidence_count": N, "verdict": "..."}}`
   - Each investigation round: `{"rca_id": "...", "event": "investigation-round-N", "data": {"gaps_filled": [...], "tools": [...]}}`
   - Each judge: `{"rca_id": "...", "event": "judge-<role>", "data": {full judge output as JSON}}`
   - Tiebreaker: `{"rca_id": "...", "event": "tiebreaker", "data": {...}}`
   - Resolution: `{"rca_id": "...", "event": "resolution", "data": {"canonical_verdict": "...", "canonical_source": "..."}}`

4. **Append MEMORY.md pointer.** If MEMORY.md doesn't exist at project root, create it with header `# Memory`. Append:
   ```
   - [RCA: <one-line target summary>](.rca/<ts>-<slug>.md) — <canonical_verdict>
   ```

5. **Emit inline summary to user:**
   ```
   RCA complete: <canonical_verdict>
   - Confidence: <high|medium|low based on judge agreement>
   - Status: <resolved|abstained|disputed>
   - Canonical source: <tiebreaker|majority-3|first-pass-unchallenged>
   - Full record: .rca/<ts>-<slug>.md
   - <If abstained:> Abstain gaps: <list>
   - <If disputed / tiebreaker fired:> Note: judges disagreed; see §4 of the record for the full dispute trace.
   ```

## Judge failure handling

After the parallel dispatch in Stage 4, classify results:

| Judges returned | Action |
|---|---|
| 3 of 3 | Standard flow. Check disagreement per Stage 5. |
| 2 of 3 | Retry the failed judge once. If still fails, proceed with disagreement check on 2 judges. Any disagreement trigger → tiebreaker fires. Note missing role in §4 of record. |
| 1 of 3 | Retry both failed once. If any still fails, force tiebreaker with the returned judge(s) + first-pass as inputs. Tiebreaker verdict is canonical. Note 2 missing roles. |
| 0 of 3 | Retry all. If still 0, status = `abstained`. Record contains first-pass + investigation log + error note. User re-invokes. |
| Tiebreaker errors | No second-level tiebreaker. Record status = `disputed`. Emit first-pass + all returned judges verbatim. User resolves manually. |

## Hard rules (non-negotiable)

1. **Advisory-only.** Never use `Write`, `Edit`, or destructive `Bash`. Never modify repo state. Never create commits.
2. **Citation-only evidence.** No paraphrased quotes, no speculative claims, no "X implies Y" without a quoted anchor.
3. **Abstain honestly.** If evidence cannot be grounded after investigation, emit `status: abstained` with explicit gap report. Do not fake a verdict.
4. **Fresh-context judges.** Judge subagents get the curated input package only (target + first-pass record + cited artifacts + investigation summary). Never pass full session history.
5. **Parallel judge dispatch.** The 3 primary judges MUST be dispatched in a single message so they run in parallel. Sequential dispatch adds unnecessary latency.
6. **Never recommend an action.** The skill produces a diagnosis. The user decides what to do.
