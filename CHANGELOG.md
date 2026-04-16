# Changelog

## [1.8.1] — 2026-04-17

### Changed
- **verification-before-completion** — One-line cleanup. Removed legacy plugin-lineage reference from "AI-Specific Failure Modes" section header. Was: *"These post-date the original superpowers version; they are documented production failures from 2024-2026."* Now: *"These are documented production failures from 2024-2026."* The temporal-provenance framing served the author, not the agent reading the skill at activation moment. Same class of cruft removed from §4.2 (Iron Law) in v1.8.0; v1.8.1 closes the inconsistency. SKILL.md still 253 lines.
- **Repo-wide:** scrubbed all references to inherited prior-plugin lineage from README, CHANGELOG, CLAUDE.md, and prior release notes (v1.8.0, v1.7.0, v1.6.0, v1.4.0). UPP is now fully self-standing in its public-facing surface — no references to legacy plugins anywhere on the repo or release pages. Replacement vocabulary: "prior version" / "inherited version" / "legacy boilerplate" / parenthetical drops.

## [1.8.0] — 2026-04-17

### Changed
- **verification-before-completion** — Full pipeline rebuild (research → synthesis → brainstorming → spec → audits → writing-plans → SKILL.md → RED-GREEN-REFACTOR → audits → deploy). Supersedes v1.7.0 which shipped earlier with documented bugs and process violations. Plan: `docs/upp/plans/2026-04-17-verification-skill-v2.md`. Spec: `docs/upp/specs/2026-04-17-verification-design-v2.md`. 6 audit log files in `audit-logs/v1.8.0-*.md` document each pipeline step.

  v1.7.0 supersession reasons (specific bugs fixed in v1.8.0):
  - **Tier 2 `git stash` bug:** v1.7.0 used `git stash` as the sole revert primitive. On a committed fix, `git stash` is a no-op — the test never went red, the negative control silently passed without verifying anything. v1.8.0 enumerates 3 cases (uncommitted, committed-HEAD, merge-commit) with state-appropriate revert commands and uses surgical `git checkout HEAD -- <files>` instead of `git reset --hard` to avoid collateral damage to unrelated dirty work.
  - **Description CSO violation:** v1.7.0 description summarized workflow ("Requires running verification commands and citing exit code"). writing-skills explicitly warned this pattern causes Claude to follow the description summary instead of reading the skill body. v1.8.0 description is pure trigger.
  - **Skipped pipeline steps:** v1.7.0 author skipped brainstorming, the writing-skills RED-GREEN-REFACTOR subagent pressure tests, the research-synthesis Phase 7 external validator subagent, and adversarial audits between steps. v1.8.0 ran all of these as structural artifacts (audit log files in `audit-logs/`).
  - **Content gaps:** v1.7.0 omitted `set -euo pipefail` mention, JUnit XML / SARIF as Rank 2 evidence, and read-back primitives by claim type. All present in v1.8.0.
  - **Inflated CHANGELOG claims:** v1.7.0 said "~40 sources" (never counted) and "each excuse bound to a real consequence" (delivered 3/10 vignettes). v1.8.0 spec §7 mandates grep-verifiable counts with no qualitative superlatives.

  v1.8.0 grep-verifiable counts (every count below independently checkable against the shipped SKILL.md):
  - SKILL.md is 253 lines (under 300 cap)
  - 5 AI failure modes (each with all 5 elements: Mechanism / Symptom / Detection signal / Mitigation / Documented incident)
  - 10 rationalization table rows
  - 4 inline incident vignettes in the rationalization table (Feb 2025 terraform destroy, TypeScript linter≠compiler example, Jul 2025 Replit DB delete, Nov 2025 Cloudflare outage)
  - 12 Red Flag bullets (preserves "subagent delegation without verification" from v1.7.0; adds "Tier 2 negative-control bypass" and "silencing the error to make verification pass")
  - 6 cache-bust ecosystem rows (Python, Node CommonJS, Node ESM, Jest, TypeScript, watch-mode runners)
  - 3 Tier 2 cases (A uncommitted, B committed-HEAD, C merge-commit)
  - 5 read-back primitive categories in Failure Mode 5 (file edit, commit/push, branch state, migration/schema, binary artifact)
  - 4 UPP integrations (test-driven-development, finishing-a-development-branch, systematic-debugging, executing-plans), no inline fallbacks
  - 0 mentions of "Builder-Validator chain" as named term (concept retained in plain language)
  - 0 legacy boilerplate phrases ("24 failure memories", "your human partner")

## [1.7.0] — 2026-04-16

### Changed
- **verification-before-completion** — Full pipeline rebuild (research → synthesis → spec → writing-skills → adversarial audits). Was: inherited from prior version as-is (139 lines, with legacy boilerplate phrases "24 failure memories" / "your human partner"). Now: 194 lines, UPP-native, AI-aware claim gate. Research: `research/19-verification-research.md` (6 topics via parallel-cli ultra-fast: false-completion patterns, exit code vs log parsing, in-session contamination, agent tool-call verification, evidence hierarchy, gate function design; ~40 sources with URLs). Synthesis: `docs/upp/brainstorms/2026-04-16-verification-synthesis.md` (FULL mode, self-validated PASS).

  Changes from inherited version:
  - **Removed** legacy boilerplate phrases ("24 failure memories", "your human partner") and the moralizing "Honesty is a core value" section.
  - **Iron Law preserved verbatim** — empirically load-bearing rhetoric (preserved per synthesis Phase 4 F3 mitigation: rationalization tables alone get treated as data; the absolute Iron Law overrides agent self-rationalization more often than procedural checklists).
  - **Gate Function rewritten** as 5 ordered steps with exit-code-first checking (was: 5 steps without explicit exit-code emphasis). Exit code emphasis sourced from research Topic B (POSIX contract; production incidents Cloudflare Nov 2025 / Clerk Jun 2025 / GitLab Jan 2025 / Jenkins CVE-2025-59476 all caused by log-string parsing instead of exit code).
  - **Tiered Evidence (new)** — Tier 1 routine claims (exit code + 1-line output) vs Tier 2 bug-fix/regression (TDD red-green negative-control sequence with `git stash` workflow). Tiering resolves over-gating anti-pattern from research Topic F.
  - **AI-Specific Failure Modes (new)** — 5 documented production failure patterns: in-session test cache contamination, log fabrication / extrapolation, sandbox failure → fabricated success, prompt injection via log content (Jenkins CVE-2025-59476), agent tool-call output deception (Replit DB delete + 4000 fabricated records, Jul 2025).
  - **Rationalization table** with inline incident vignettes — terraform destroy 1.94M rows (Feb 2025), Replit DB delete (Jul 2025), Cloudflare outage (Nov 2025) — each binds an excuse to a real consequence (research Topic D production incident reports).
  - **UPP Integration (new)** — 4 explicit pairings, each verified against UPP plugin inventory + each with inline fallback: `test-driven-development` (Tier 2 negative control), `finishing-a-development-branch` (defers branch-level test invocation to its Step 1a), `systematic-debugging` (root cause vs workaround when verification fails), `executing-plans` (per-task gate).
  - **Common Mistakes (new)** — 5 specific patterns: log-text inference, in-session retesting, trusting agent tool-call output, silencing errors instead of fixing, skipping TDD red phase.

  Brainstorming was skipped intentionally for this rebuild — synthesis encoded all design decisions across 6 research topics + competing-hypothesis selection + adversarial pre-mortem + self-validated PASS. No discovery questions remained open.

## [1.6.0] — 2026-04-16

### Changed
- **finishing-a-development-branch** — Full pipeline rebuild (research synthesis → brainstorm → spec → writing-skills → adversarial audits). Research: `research/17-finishing-branch-research.md` (6 topics, ~30 sources with URLs). Seven research-backed additions to v1.4.1:
  - **Step 1a** mandates FRESH TERMINAL test re-run with pasted exit code — addresses in-session hallucinated "all tests passed" claims.
  - **Step 1e (new)** diff self-consistency check scans for suspicious infra/config file changes (`package.json`, `tsconfig.json`, `.github/workflows/`, etc.) — catches AI workarounds (e.g., bumping a package version to silence an error instead of fixing the bug).
  - **Step 2.5 (new)** size advisory: fires when >400 LOC AND >3 commits. Cites Propel Code data (defect escape rate 4%→28% between 200 and 800 LOC). Advisory only, does not block.
  - **Step 3** audience detection: if remote + CI detected, prepends note advising Option 2 (PR) over Option 1 (local merge) since local merge skips CI verification.
  - **Step 4 Option 1** now asks merge strategy (squash vs merge-commit) with commit-count default and rebase-merge parenthetical. Sources: GitHub docs, kernel.org.
  - **Step 4 Option 2** expanded PR body template: required Summary, Linked Issue, Test Plan (includes fresh-terminal checkbox), Rollback; optional AI provenance comment line.
  - **Step 5** pre-removal worktree checklist: `git status` clean, commits pushed, branch state known. Surfaces `git worktree remove` refusal instead of force-removing silently.
  - Expanded Common Mistakes, Red Flags, and new Rationalizations table. Kept v1.4.1's correct Step 1c (linter for imports, scoped grep for debug statements) and Step 1d (design-system-enforcer reference). 244 → 394 lines.

### Added
- **using-git-worktrees** — New UPP skill. Full pipeline build (research → synthesis → spec → writing-skills). Research: `research/18-git-worktrees-research.md` (5 topics: internals, bare-repo pattern, pitfalls, Claude Code native support, pool pattern; ~25 sources with URLs). Progressive-disclosure structure:
  - **Mental Model** — shared objects + refs, independent HEAD/index, `.git`-as-file pointer, same-branch invariant.
  - **When to Use** — decision table + scale thresholds (1-4 raw commands / 5-10 scripted / >10 pool).
  - **Primary Path — Claude Code Native** — `--worktree` flag, `isolation: worktree` agent frontmatter, EnterWorktree/ExitWorktree pattern. Every native path paired with raw-git equivalent to insulate from API rename.
  - **Raw Git Path** — create / list / remove / prune / lock + pre-removal checklist.
  - **7 Top Pitfalls** — same-branch invariant, node_modules duplication (pnpm fix), hooks + `core.hooksPath`, nested-worktree anti-pattern, concurrent `gc` corruption, tool compatibility, Windows path length.
  - **Advanced Patterns (reference)** — bare-repo pro pattern (fsck.sh), pool pattern (Worktrunk, workmux), sparse-checkout combo. Each ~8 lines with tooling pointer.
  - Quick Reference tables, Red Flags, Rationalizations table, Integration section (called by dispatching-parallel-agents, pairs with finishing-a-development-branch). 331 lines.
- **dispatching-parallel-agents** — Updated the `using-git-worktrees` reference from "if skill not yet available" to "invoke for full lifecycle" now that the skill exists (fallback one-liner retained as defensive coding). 208 → 209 lines.

## [1.5.0] — 2026-04-16

### Changed
- **dispatching-parallel-agents** — Full pipeline rebuild (research synthesis → brainstorm → spec → writing-skills → adversarial audits). File ownership dual-path (pipeline: from plan, standalone: agent determines during decomposition with overlap detection). Sequential merge fixed: tests between each merge, not after all — if tests fail post-merge, revert last merge, investigate, re-merge. "Don't fix other agents' errors" rule added to agent prompt template. Failure handling: revert partial edits from failed agent, merge successful, create new task. Worktree isolation recommendation with concrete triggers + inline fallback. Cost awareness with context window rationale. Real Example updated to demonstrate between-each-merge procedure. 195 → 208 lines.

## [1.4.1] — 2026-04-16

### Fixed
- **finishing-a-development-branch** — Step 1c grep was hardcoded to `src/`, now scans changed files only via `git diff main --name-only`. Stale import detection now references linter instead of grep (grep can't catch unused imports). TODO/FIXME scan now checks only lines added in this branch (not pre-existing TODOs). Dead code detection references `knip` or project-specific tools.
- **finishing-a-development-branch** — Step 1d design compliance now references design-system-enforcer skill explicitly and includes a concrete grep command for hardcoded hex colors. Previously unexecutable.
- **finishing-a-development-branch** — Added cross-references to verification-before-completion and design-system-enforcer in Integration section.
- **dispatching-parallel-agents** — Agent prompt example updated to demonstrate file ownership declaration and shared spec reference (previously taught the concept but didn't show it).

## [1.4.0] — 2026-04-16

### Changed
- **dispatching-parallel-agents** — Added file ownership declaration in agent task creation (prevents conflicts instead of detecting them), shared spec reference for coordination, sequential merge strategy in review/integrate step, AI-specific spot checks. 183 → 185 lines.
- **finishing-a-development-branch** — Expanded Step 1 from "verify tests" to full pre-completion verification: tests + lint/type checks + AI completeness scan (stale imports, dead code, leftover debug statements, config artifacts) + design compliance gate (when DESIGN.md exists). Added "premature done claim" to common mistakes. Updated red flags for expanded verification. 201 → 235 lines.

### Added
- **finishing-a-development-branch** — New skill in UPP, enhanced with AI-aware pre-completion verification.

## [1.3.0] — 2026-04-16

### Changed
- **systematic-debugging** — Enhanced with AI-aware debugging patterns and escalation ladder. Phase 1 restructured from sequential numbered steps to parallel investigation checklist. Added AI-generated code failure patterns (hallucinated APIs, happy-path handlers, silent failures, missing edge cases, training data mismatch). Added error misdirection check ("don't trust where the error says it is"). New 3-rung escalation ladder: fix 1 → new hypothesis, fix 2 → hypothesis-generator subagent (fresh context, constrained input), fix 3 → question architecture. New Impact Analysis subsection (upstream/downstream/boundary/observability checks before committing fix). 296 → 301 lines.

## [1.2.0] — 2026-04-16

### Changed
- **test-driven-development** — Enhanced with agent-aware TDD patterns. Added "Test Behaviors, Not Implementations" as first principle with 4-row boundary examples table. Added test-reviewer agent gate in RED phase (mandatory for >3 test cases). Expanded REFACTOR from 3 lines to full subsection. Added spec-to-test connection for UPP pipeline. Updated exceptions ("scaffolding output" not "generated code"), When Stuck (agent-first guidance), verification checklist (test-reviewer line). 372 → 433 lines.
- **executing-plans** — Updated Integration section to reference test-reviewer agent in subagent TDD flow. Added REFACTOR step to flow description. Aligned skip threshold with TDD skill (>3 test cases in a single file).

### Added
- **test-reviewer agent** — New agent definition (agents/test-reviewer.md, 120 lines). Fresh-context test quality reviewer dispatched as gate in TDD RED phase. Checks: trivial passability, behavior vs implementation assertions, missing edge cases, mock quality, spec alignment. Explicit context isolation — rejects implementation hints from dispatch payload.

## [1.1.0] — 2026-04-16

### Changed
- **using-upp** — Rebuilt from ground up. Added product development pipeline state machine (graphviz), enforcement-oriented routing table with "MUST invoke" and "Why — what goes wrong if you skip" columns, signal-based self-check protocol for mid-session skill awareness, action-oriented "Do This Instead" column on red flags table. Positional optimization: signals + self-check in recency zone for maximum LLM attention retention. 130 → 230 lines.

## [1.0.0] — 2026-04-15

Initial release of Ultimate Product Powers.

### Core Pipeline
- **brainstorming** — Prototype-first brainstorming with 5-lens + Design & UX discovery. Stitch mood exploration → v0 prototype generation → DESIGN.md extraction → Figma enrichment → Playwright baselines.
- **writing-plans** — Design-aware implementation planning. Design Context detection, bottom-up task ordering, two task shapes (standard + design-aware), golden samples tasks for agentic products, progressive verification (mid-plan spot-check + final).
- **executing-plans** — Unified plan execution merging inline and subagent modes. Micro-manifest context packaging (8 fields), three-gate review pipeline (spec compliance → code quality → design compliance), fix iterations with 3-cycle termination, design spot-check dispatch, final holistic code review.

### Design & Frontend
- **design-system-enforcer** — DESIGN.md grounding with 4-layer enforcement. Golden samples system for agentic products. Figma drift detection.
- **product-redesign** — Two-phase frontend overhaul: Diagnosis (scan → pain → vision → exit gate) then Treatment (audit → prototypes → DESIGN.md → migration strategy).
- **agentic-ux-patterns** — Reference patterns for agent UI: streaming strategies, approval flows, error recovery, streaming accessibility, responsive agent UI.

### Engineering Discipline
- **test-driven-development** — TDD with Iron Law enforcement. Red-Green-Refactor cycle. Adopted unmodified from prior version.
- **systematic-debugging** — Four-phase root cause methodology with 3-fix escalation rule. Includes root-cause-tracing, defense-in-depth, and condition-based-waiting references.
- **verification-before-completion** — Evidence-before-claims discipline. Adopted unmodified from prior version.

### Code Review
- **requesting-code-review** — Review dispatch workflow with mandatory triggers and code-reviewer agent integration.
- **receiving-code-review** — Review response discipline: no performative agreement, verify before implementing, push back when wrong. Adopted unmodified from prior version.

### Meta
- **writing-skills** — TDD methodology for skill authoring with skill type assessment (process vs expertise vs hybrid), CSO, pressure testing, graphviz conventions.
- **dispatching-parallel-agents** — Parallel subagent dispatch with independence decision flowchart. Adopted unmodified from prior version.
- **using-upp** — Skill discovery guide with 13-skill routing table, 1% enforcement rule, red flags table. Auto-injected at session start.

### Hooks
- **SessionStart** — Combined skill discovery injection + DESIGN.md state detection + token digest caching.
- **PreToolUse** (Write|Edit) — Design token injection on component/page file writes with per-session deduplication.
- **SubagentStart** — Design token injection to every subagent.

### Agent
- **code-reviewer** — Design-aware senior code reviewer. Checks plan alignment, code quality, architecture, and design compliance (semantic tokens, typography, component patterns, accessibility, Section 10) when DESIGN.md exists.

### Infrastructure
- Self-hosted marketplace via `marketplace.json`
- Cross-platform hook wrapper (`run-hook.cmd` — Unix + Windows)
- v0 prototype generation wrapper (`v0-generate.mjs`)
