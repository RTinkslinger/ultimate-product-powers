---
name: requesting-code-review
description: Use when completing tasks, implementing features, or before merging to request independent code review
---

# Requesting Code Review

## Core Principle

Review early, review often. Every review request bundles verifiable evidence and dispatches to an independent reviewer. Fresh context catches what same-context misses.

**Announce:** "I'm using the requesting-code-review skill to request review."

## Mandatory Triggers

These trigger conditions require requesting review. Skip-allowed = No for all.

| # | Trigger | Condition | Verification |
|---|---------|-----------|-------------|
| 1 | **Plan task completion** | Completing any task in executing-plans | Plan task ID referenced in evidence bundle |
| 2 | **Pre-merge** | Before merge to main or any protected branch | `git log --oneline main..HEAD` included |
| 3 | **Security-sensitive** | Changes to auth, data/PII, IaC, API contracts, encryption, access control | File paths in diff touching relevant code |
| 4 | **Scale threshold** | Diff ≥200 LOC OR changes touch ≥3 modules | `git diff --stat` line count confirms |

**Optional triggers** (valuable but not enforced):
- When stuck and need fresh perspective
- Before starting a major refactoring (baseline check)
- After fixing a complex or hard-to-reproduce bug

## Evidence Bundle

Every review request includes a structured evidence bundle. The reviewer evaluates the work product, not the thought process.

```
EVIDENCE BUNDLE:

  what_was_implemented:   Description of change (1-3 sentences)
  spec_or_requirements:   Plan task reference, spec section, or acceptance criteria
  diff:
    base_sha:             Starting commit (origin/main or task-start SHA)
    head_sha:             Current HEAD
    scope:                Files changed (from git diff --stat)
  test_evidence:
    exit_code:            0 (passing) — from verification-before-completion
    runner_output:        1-line excerpt or structured artifact (JUnit XML, SARIF)
    coverage_delta:       Baseline → new (if tracked)
    negative_control:     If bug-fix: red + green exit codes (Tier 2)
  design_compliance:      (only if DESIGN.md exists AND UI changes made)
    token_compliance:     Pass/fail against DESIGN.md Sections 2-4
    visual_snapshot:      If available
  audit_logs:             (only if produced during implementation)
    paths:                List of audit-log file paths
```

**Redaction rule (mandatory):**
- NO builder chain-of-thought
- NO scratchpad or internal deliberation
- NO conversation history or discarded approaches
- Bundle contains ARTIFACTS ONLY

Evidence vocabulary: falsifiable artifact = exit code, test runner output, git SHA, diff, coverage delta, SARIF. Self-report ("tests pass") is the weakest tier.

## Agent Dispatch Protocol

```
1. SELECT reviewer:
   Default:      code-reviewer agent (always — UPP's design-aware reviewer)
   Add:          test-reviewer agent (when task involved TDD or test changes)
   Request:      design-compliance review (when DESIGN.md exists AND diff touches UI)

2. BUILD evidence bundle per schema above. Apply risk tier to determine depth.

3. DISPATCH via Agent tool:
   - Fresh context. No prior conversation. Builder ≠ reviewer.
   - Prompt includes: what_was_implemented, spec_or_requirements, base + head SHAs
   - Attach diff and test evidence inline (not as file paths)
   - System instruction: "Evaluate supplied artifact only. Do not consider prior reasoning."

4. RECEIVE findings:
   - Auto-chain: receiving-code-review fires on inbound findings.
   - Reviewer findings are processed per receiving skill's Response Chain.

5. ACT on findings:
   - Critical: fix immediately before any other work
   - Important: fix before proceeding to next task
   - Minor: note for later (or fix if quick)
   - Pushback: apply receiving skill's evidence-based pushback protocol
```

## Risk-Tiered Bundling

The risk tier determines bundle depth, NOT whether review happens. All tiers dispatch a reviewer.

| Risk | Criteria | Bundle depth |
|---|---|---|
| **Low** | ≤5 LOC, cosmetic, docs, formatting | Diff + one-liner description |
| **Medium** | Functional changes, moderate scope, <200 LOC | Diff + spec/requirements + test evidence |
| **High** | Security, data/PII, API contracts, ≥200 LOC, ≥3 modules | Full bundle: diff + spec + tests + negative controls + audit logs + design compliance |

"Low risk = skip review" is an anti-pattern. Low risk = lighter bundle, same review discipline.

Risk tiers: Low (≤5 LOC, cosmetic), Medium (functional, moderate scope), High (security, data, API, ≥200 LOC, ≥3 modules).

## Auto-Chain to Receiving

When this skill dispatches a reviewer agent and findings return:

1. The receiving-code-review skill fires automatically on the inbound findings.
2. Findings are triaged by severity × confidence × blast_radius.
3. Each finding is processed through receiving's Response Chain (verify → evaluate → respond → implement).
4. After all findings are addressed, the review cycle is complete.

This auto-chain means: request review once, and the full receive→process→implement loop follows without manual invocation.

## Integration Points

**executing-plans** — This skill fires at the quality gate in the three-gate review pipeline. When a plan task is complete, requesting-code-review bundles the task's evidence and dispatches the reviewer before the task is marked done.

**finishing-a-development-branch** — This skill fires at Step 1 (pre-merge checklist). Before merging to main, a review must be requested with the full branch diff as evidence.

**verification-before-completion** — The evidence bundle references Tier 2 artifacts from verification (exit codes, negative controls). The two skills are complementary: verification produces the evidence, requesting bundles it for the reviewer.

## Red Flags

You are about to violate this skill if you catch yourself doing any of these. STOP:

- About to skip review because "it's simple" or "just a small change"
- Self-reviewing from the same context instead of dispatching a fresh-context agent
- Submitting a thin evidence bundle (diff only, no test evidence, no spec reference)
- About to merge without requesting review (mandatory trigger #2)
- Dispatching reviewer WITHOUT redacting builder's chain-of-thought
- Security-sensitive change without flagging it as such in the review request
- Proceeding with unfixed Critical or Important findings from reviewer
- Arguing with valid technical feedback instead of citing evidence

## The Bottom Line

Bundle evidence. Dispatch independent reviewer. Fresh context, always.
