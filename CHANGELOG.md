# Changelog

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
