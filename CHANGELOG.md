# Changelog

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
- **using-git-worktrees** — New UPP skill (previously only in disabled superpowers). Full pipeline build (research → synthesis → spec → writing-skills). Research: `research/18-git-worktrees-research.md` (5 topics: internals, bare-repo pattern, pitfalls, Claude Code native support, pool pattern; ~25 sources with URLs). Progressive-disclosure structure:
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
- **finishing-a-development-branch** — New skill in UPP (previously superpowers-only). Enhanced with AI-aware pre-completion verification.

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
- **test-driven-development** — TDD with Iron Law enforcement. Red-Green-Refactor cycle. Adopted from superpowers (zero modifications).
- **systematic-debugging** — Four-phase root cause methodology with 3-fix escalation rule. Includes root-cause-tracing, defense-in-depth, and condition-based-waiting references.
- **verification-before-completion** — Evidence-before-claims discipline. Adopted from superpowers (zero modifications).

### Code Review
- **requesting-code-review** — Review dispatch workflow with mandatory triggers and code-reviewer agent integration.
- **receiving-code-review** — Review response discipline: no performative agreement, verify before implementing, push back when wrong. Adopted from superpowers (zero modifications).

### Meta
- **writing-skills** — Synthesized from superpowers writing-skills + SKILL-CRAFT methodology. TDD for skill authoring with skill type assessment (process vs expertise vs hybrid), CSO, pressure testing, graphviz conventions.
- **dispatching-parallel-agents** — Parallel subagent dispatch with independence decision flowchart. Adopted from superpowers (zero modifications).
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
