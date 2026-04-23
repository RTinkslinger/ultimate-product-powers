# Changelog

## [2.2.0] — 2026-04-24

Test-discipline hardening. Expands `test-reviewer` agent from 5 to 9 checks, introduces new `test-reviewer-fast` sibling for ≤3 test suites, and upgrades the TDD skill with explicit Chicago-school stance + production-boundary testing guidance + soft-medium gates.

### Added

- `agents/test-reviewer-fast.md` — 3-check fast-mode variant (Production Call-Site, Description-Behavior, Oracle Strength) for ≤3 test suites. Dispatched automatically by the TDD skill based on suite size.
- TDD skill: **Chicago-School TDD** section making the stance explicit. UPP tests real code through real boundaries; mocks only for truly external/slow I/O. Wrapped in `<HARD-GATE>` (G3).
- TDD skill: **Testing Through the Production Boundary** section with HTTP/MCP-stdio/MCP-SSE/CLI/framework-hook table and the test-through-the-public-API rule. Wrapped in `<HARD-GATE>` (G3).
- TDD skill: **Going Further: Mutation Testing** recommended (not mandatory) section pointing to Stryker / PIT / mutmut / cargo-mutants / Infection.
- `testing-anti-patterns.md` rewritten as 9-pathology catalog with industry terms, detection signals, bad/good examples, reviewer-flag mapping, and literature citations. Includes Quick Reference flag→pathology→remediation table.

### Changed

- `agents/test-reviewer.md` — expanded from 5 checks to 9. New: **Production Call-Site Verification** (UNWIRED), **Description-Behavior Correspondence** (UNVERIFIED CLAIM), **Oracle Strength** (WEAK ORACLE + 5 subtypes), **Lifecycle/Workflow Coverage** (always runs, emits `N/A — stateless feature` when not applicable). Refined: Check 3 splits Error-Path Parity explicitly; Check 4 adds self-fulfilling-mock detection and per-test path heuristic.
- Output format is now **severity-tiered**: CRITICAL (blocks GREEN), MAJOR (review inline), ADVISORY (non-gating).
- **Graceful degradation**: reviewer emits `INSUFFICIENT CONTEXT` when dispatcher can't provide SUT source or entry-point hint, runs the checks that don't need the missing input.
- **Self-fulfilling mocks fire in BOTH** Check 4 (`MOCK SMELL: self-fulfilling`) AND Check 8 (`WEAK ORACLE: self-fulfilling`) — intentional double-flagging so the pattern is caught regardless of mental model.
- TDD skill: `When to skip: Only for ≤3 test cases` → **non-skippable gate** with mode dispatch. ≤3 tests → fast reviewer; >3 tests → full reviewer. No bypass path.
- TDD skill: **REVISE verdict is a full stop** (G5 gate). No GREEN with open CRITICAL findings.
- TDD skill: **Verification Checklist** requires the reviewer's summary block pasted as a literal artifact (G4 trap).
- TDD skill: three sections wrapped in `<HARD-GATE>` markdown (G3): Test-Reviewer Gate, Chicago-School TDD, Testing Through the Production Boundary.
- TDD skill: `Why Order Matters` section shrunk from ~50 lines to ~5 (content preserved in Common Rationalizations table; reclaims room for Chicago + Production Boundary sections).
- TDD skill: Red-Green-Refactor flow diagram updated to dispatch by suite size with REVISE hard-stop edges.
- TDD skill: Common Rationalizations table adds refutation for "this suite is small, skip the reviewer."

### Rationale

Driven by Safari Pilot codebase audit (58 findings across 7 recurring patterns) plus research synthesis across 4 parallel ultra-mode tracks (~3000 lines) documenting 9 LLM-test pathologies with industry-standard terminology. Full decision log in the dev repo at:
- `docs/upp/specs/2026-04-24-test-discipline-hardening-v2.md`
- `docs/superpowers/brainstorms/2026-04-24-test-discipline-hardening-synthesis.md`
- `research/23-test-discipline-synthesis.md`

### Validation

8-fixture Safari-Pilot-derived test battery in dev repo at `tests/fixtures/test-discipline-v2/`. Each fixture is a `{test.ts, sut.ts, spec.md, expected-review.md}` triple demonstrating one pattern. Phase 7 spot-checks confirmed v2 agent correctly flags UNWIRED, UNVERIFIED CLAIM, WEAK ORACLE (all subtypes), and the self-fulfilling-mock double-flag across Checks 4 and 8.

### Not in this release (deferred to v2.3)

- Workflow-state hooks (Stop hook blocking session end if reviewer not invoked; PreToolUse hook on test runners). Deferred pending post-v2 telemetry on LLM bypass behavior.

### Not shipping (rejected in brainstorming)

- Commit-time mock-ban hook (content-judgment static detector). No foolproof path-based / import-based / annotation-based approach exists; all have structural false-positive/negative problems. Semantic judgment at review time (Check 4 path heuristic + Chicago stance + Production Boundary section) replaces static detection.

---

## [2.1.0] — 2026-04-21
Added: rca skill + rca-judge agent (user-invoked disciplined RCA)
- rca: advisory-only `/rca <target>` command. Produces grounded root-cause analysis on any target (bug, failing test, file, error, commit, prior diagnosis). Full flow: intake + ambiguity survey → query neutralization → first-pass ACH (≥3 hypotheses, citation-only evidence, inconsistency matrix, falsification criterion) → read-only investigation loop (10-round cap, abstain on non-convergence) → 3 parallel fresh-context judges (skeptic, evidence-auditor, safety-evaluator) with CLEV tiebreaker on disagreement or critical flag → canonical hypothesis record at `.rca/<ts>-<slug>.md` + telemetry JSONL + MEMORY.md pointer. Never mutates repo state.
- rca-judge: single parameterized judge agent (role = skeptic | evidence-auditor | safety-evaluator | tiebreaker). Receives curated input package (target + first-pass record + cited artifacts), NOT full session. Produces fresh independent verdict + delta-score on first-pass + RULERS rubric + flags + final verdict per role prompt.
- Research basis: 10-track parallel study (~605KB, 150K tokens) + full evidence extraction + adversarial-validated synthesis. Leans on G2 query neutralization (63%→39% sycophancy), F9 curated input package, F15 RULERS rubric (Spearman >0.80 with expert), F6 CLEV cascade, K7 canonical record schema.
- Plugin: 18 skills, 4 agents, 3 hooks

## [2.0.0] — 2026-04-17
Added: security-review skill, security-reviewer agent, test infrastructure
- security-review: 3-step security gate (threat-model, scan, cite evidence), per-language SAST command table (5 ecosystems), Iron Law severity enforcement (critical/high = hard block), 6 AI-specific threat categories (prompt injection, slopsquatting, insecure output handling, config-as-attack-surface, tool poisoning, agent trust boundaries), 10x hardened slopsquatting verification protocol, secrets detection with rotation guidance, always-dispatch security-reviewer agent
- security-reviewer: adversarial reviewer in independent context, 6 AI-threat deep dives with grep detection patterns, independent SAST scan protocol, 5-dimension adversarial checklist, structured output format
- Test infrastructure: pytest harness with 98 tests across 4 layers — L1 content snapshots (20 tests, gating), L2 trigger tests (68 tests, xfail informational), L3 behavior RED-GREEN (6 tests, xfail informational), hook smoke tests (4 tests, gating). Pre-push hook gates on L1 + hooks (24 tests, <15s)
- Plugin: 17 skills, 3 agents, 3 hooks

## [1.9.0] — 2026-04-17
Edited: receiving-code-review, requesting-code-review (UPP-native rebuild)
- receiving: 6-step response chain with inline rationalization traps, 5 AI failure modes, structured/prose dual-path feedback handling, 3-source handling (user/AI agent/external), conditional routing to 3 UPP skills, deadlock resolution via second-opinion agent, 12 red flags
- requesting: 4 mandatory trigger categories (all skip=No), canonical evidence bundle with redaction rule, agent dispatch protocol with fresh-context enforcement, 3 risk tiers, auto-chain to receiving, 8 red flags
- Voice: "your human partner" framing replaced with role-neutral language throughout
- Removed: Circle K easter egg, GitHub thread reply section, inline bash for SHA retrieval

## [1.8.1] — 2026-04-17
Edited: verification-before-completion (one-line cleanup)

## [1.8.0] — 2026-04-17
Edited: verification-before-completion (full pipeline rebuild, supersedes v1.7.0)

## [1.7.0] — 2026-04-16
Edited: verification-before-completion (superseded by v1.8.0)

## [1.6.0] — 2026-04-16
Added: using-git-worktrees
Edited: finishing-a-development-branch, dispatching-parallel-agents

## [1.5.0] — 2026-04-16
Edited: dispatching-parallel-agents

## [1.4.1] — 2026-04-16
Fixed: finishing-a-development-branch, dispatching-parallel-agents

## [1.4.0] — 2026-04-16
Added: finishing-a-development-branch
Edited: dispatching-parallel-agents

## [1.3.0] — 2026-04-16
Edited: systematic-debugging

## [1.2.0] — 2026-04-16
Edited: test-driven-development, executing-plans

## [1.1.0] — 2026-04-16
Edited: using-upp

## [1.0.0] — 2026-04-15
Initial release. Skills:

- brainstorming
- writing-plans
- executing-plans
- design-system-enforcer
- product-redesign
- agentic-ux-patterns
- test-driven-development
- systematic-debugging
- verification-before-completion
- requesting-code-review
- receiving-code-review
- writing-skills
- dispatching-parallel-agents
- using-upp
