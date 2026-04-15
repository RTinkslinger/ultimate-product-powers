# Changelog

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
