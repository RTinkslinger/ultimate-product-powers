# Canonical Hypothesis Record — v1 Schema

Every `/rca` invocation produces one record at `.rca/<ISO-timestamp>-<slug>.md`. This is the authoritative format.

## Frontmatter (required)

```yaml
---
rca_id: <uuid v4>
created: <ISO 8601 timestamp, e.g. 2026-04-21T14:23:00Z>
target: "<user's argument, verbatim>"
target_type: path | description | test | commit | log | other
status: resolved | abstained | disputed
verdict: "<leading hypothesis, one line>" | abstain
canonical_source: tiebreaker | majority-3 | first-pass-unchallenged
judge_agreement: <percentage or "n/a">
investigation_rounds: <integer >= 0>
---
```

All keys are required. `verdict` = `abstain` iff `status` != `resolved`.

## Body sections (required order)

### 1. Neutralized query

One paragraph. Rewrite of the user's target that strips user framing (e.g., "why does X fail?" → "reproduction + failure mode of X"). Preserves semantic intent.

### 2. First-pass analysis

Three sub-sections, all required.

#### Hypotheses

Markdown list. At least 3 items, each formatted:

```markdown
- **H<N>:** <claim, one sentence>
  - Confidence: low | medium | high — <grounded reasoning>
  - Falsification criterion: <specific observable>
```

#### Evidence table

Markdown table, at least one data row. Every row must have a non-empty `source`:

```markdown
| id | quote | source | supports | refutes |
|---|---|---|---|---|
| E<N> | "<exact quote>" | <path:line or log:timestamp> | <H list or empty> | <H list or empty> |
```

#### Inconsistency matrix

Markdown table, hypotheses as columns, evidence ids as rows. Cells: `✓` (supports), `✗` (refutes), `?` (irrelevant or unknown). At least 60% of cells filled (not `?`).

#### First-pass verdict

One paragraph. Names the leading hypothesis + confidence level + terse reasoning chain.

### 3. Investigation log

Numbered list. Each round:

```markdown
- **Round <N>** (reason: <gap identifiers>):
  - Tools: <tool_name>(<args>) → <result summary>
  - New evidence: E<N>, E<N+1>
```

Ends with:

```markdown
- **Stop reason:** converged | hypothesis-space-narrowed | hypothesis-space-exhausted | max-rounds (abstained)
```

If no investigation rounds ran (first-pass converged immediately), log shows `Round 1 (skipped): first-pass converged`.

### 4. Judge pass

Four sub-sections: Judge 1 (skeptic), Judge 2 (evidence-auditor), Judge 3 (safety-evaluator), Disagreement + optional Tiebreaker.

Each judge sub-section:

```markdown
### Judge <N> — <role>
- Fresh verdict: <hypothesis + verdict, one paragraph>
- Delta on first-pass: <agreement/disagreement per point>
- (evidence-auditor only) Citation-resolution check: E1 ✓, E2 ✗ (<why>)
- (safety-evaluator only) Worst-case-if-actioned: <description>
- RULERS rubric: H-gen: N/5, alt: N/5, evidence: N/5, completeness: N/5, stopping: N/5, safety: N/5
- Flags: critical | warning | none — <description if not none>
- Final verdict: accept | accept-with-caveats | reject
```

If a judge failed to return (retry also failed), show:

```markdown
### Judge <N> — <role>
- Status: FAILED (both attempts errored; see telemetry for details)
```

Disagreement block:

```markdown
### Disagreement
- Fired: yes | no
- Reason: <"verdict mismatch across judges" | "critical flag from Judge <N>" | "first-pass vs majority disagreement" | "n/a">
```

Tiebreaker block (only if fired):

```markdown
### Tiebreaker
- Fresh verdict: ...
- Combined rubric: ...
- Arbitration reasoning: ...
- Final verdict: accept | accept-with-caveats | reject
```

### 5. Resolution

```markdown
- **Canonical verdict:** <leading hypothesis> | abstain
- **Canonical source:** tiebreaker | majority-3 | first-pass-unchallenged
- **Causal chain:** <evidence ids> → <hypothesis> → <implication>
- **Falsification criterion:** <what would change this verdict>
- **Abstain gaps** (if status=abstained): <what evidence would be needed; enumerate>
```

### 6. References

```markdown
- Files read: <list of paths>
- Tools invoked: <tool_name: count>, ...
- Commits examined: <SHA list or "n/a">
- Session turns referenced: <turn index list or "none">
```

## Validation

See `docs/upp/specs/scripts/validate_record.py` for automated checks:
- Frontmatter completeness + value constraints
- Required sections present
- ≥ 3 hypotheses
- Every evidence row has non-empty source
