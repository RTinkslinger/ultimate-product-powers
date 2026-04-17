# Ultimate Product Powers (UPP)

**Design-aware product development skills for Claude Code.**

UPP is a Claude Code plugin that covers the full product development lifecycle — from brainstorming ideas into working designs, through implementation planning, to multi-agent execution with design-compliant code review. It ships 17 skills, 3 agents, and 3 hooks that work together as a coordinated pipeline.

What makes UPP different from general-purpose coding skills: **design is a first-class concern throughout.** When you build frontends, UPP's brainstorming generates working prototypes and extracts a DESIGN.md that flows through every subsequent skill. Plans order tasks by design dependency. Subagents receive design tokens in their context. Code review checks component compliance against the spec. When you build backends or non-UI projects, the design layer silently deactivates and the engineering discipline skills take over.

---

## Quick Start

### Install

```bash
/plugin marketplace add RTinkslinger/ultimate-product-powers
```

That's it. All 17 skills, 3 agents, and 3 hooks are immediately available.

### Update

```bash
/plugin update ultimate-product-powers
```

### Verify installation

After installing, start a new Claude Code session. You should see UPP's `using-upp` skill fire automatically — it injects itself at session start via the SessionStart hook and prints a brief routing guide. If you see UPP skills listed in your available skills, you're set.

---

## How the Pipeline Works

UPP skills form a state machine. Each skill knows where it fits and what comes next.

```
  User request
       │
       ▼
  ┌─────────────┐    ┌──────────────────┐
  │ brainstorming│───▶│   writing-plans   │
  │ (5+ lenses)  │    │ (design-aware)    │
  └──────┬───────┘    └────────┬──────────┘
         │                     │
    Produces:             Produces:
    - Spec                - Implementation plan
    - DESIGN.md           - Task ordering
    - Prototypes          - Verification steps
         │                     │
         ▼                     ▼
  ┌──────────────────────────────────────────┐
  │            executing-plans                │
  │  ┌────────────────────────────────────┐  │
  │  │  For each task:                     │  │
  │  │  1. test-driven-development (RED)   │  │
  │  │  2. Implement (GREEN)               │  │
  │  │  3. verification-before-completion  │  │
  │  │  4. requesting-code-review          │  │
  │  │     └─▶ code-reviewer agent         │  │
  │  │         └─▶ receiving-code-review   │  │
  │  │  5. Next task                       │  │
  │  └────────────────────────────────────┘  │
  └──────────────────────────────────────────┘
         │
         ▼
  ┌──────────────────────┐
  │ finishing-a-branch    │
  │ (merge / PR / clean)  │
  └───────────────────────┘
```

### The chain in detail

1. **You describe what you want to build.** UPP's `using-upp` skill (auto-injected at session start) routes you to the right entry point.

2. **Brainstorming** explores the problem through 5 discovery lenses (Architecture, UX, Edge Cases, Scope, Integration). For frontend projects, it detects whether DESIGN.md exists — if not, it enters prototype-first mode: Stitch generates mood boards, v0 generates working prototypes, you pick one in the browser, and DESIGN.md is extracted from the chosen prototype. The output is a design spec.

3. **Writing-plans** reads the spec and produces a detailed implementation plan. When DESIGN.md exists, tasks are ordered by design dependency (tokens → shared components → composed components → pages), each task gets a design reference block pointing to specific DESIGN.md sections, and progressive verification tasks are inserted.

4. **Executing-plans** runs the plan task by task. It supports two modes:
   - **Subagent mode** (recommended): spawns a fresh subagent per task with a structured micro-manifest (task spec, file context, design tokens). Each completed task goes through a three-gate review: spec compliance → code quality → design compliance.
   - **Inline mode**: executes tasks in the current session with periodic checkpoints.

5. **During execution**, multiple skills fire per task:
   - `test-driven-development` enforces RED-GREEN-REFACTOR
   - `verification-before-completion` gates every "done" claim on fresh evidence (exit code, not log text)
   - `requesting-code-review` bundles evidence and dispatches the `code-reviewer` agent
   - `receiving-code-review` fires automatically when reviewer findings return (auto-chain) and processes each finding with technical rigor

6. **Finishing-a-development-branch** runs pre-merge verification, presents integration options (merge, PR, worktree cleanup), and handles the chosen workflow.

### Skills that fire independently

Not everything is part of the linear pipeline. These skills fire on their own triggers:

- `systematic-debugging` — fires when you encounter a bug, test failure, or unexpected behavior
- `using-git-worktrees` — fires when you need parallel branch checkouts or filesystem isolation
- `dispatching-parallel-agents` — fires when you have 2+ independent tasks that can run concurrently
- `product-redesign` — fires when overhauling an existing frontend's design system
- `agentic-ux-patterns` — reference skill for agent UI patterns (streaming, approval flows, error recovery)
- `writing-skills` — meta-skill for authoring new skills (TDD applied to skill development)

---

## Skills Reference

### Core Pipeline Skills

#### brainstorming
**Lines:** 543 | **Trigger:** New feature, new project, or idea that needs design exploration

Turns ideas into fully formed designs through collaborative dialogue. Explores through 5 discovery lenses using multiple-choice questions, then proposes 2-3 approaches with tradeoffs.

**Modes:**
- **Standard mode** (no frontend, or frontend with existing DESIGN.md): 5-lens discovery → approaches → design presentation → spec document
- **Prototype-first mode** (greenfield frontend, no DESIGN.md): adds a 6th Design & UX lens (3-5 questions on visual direction, IA, agent output, interaction states, density), then runs the Prototype-First Pipeline: Stitch mood exploration → v0 prototype generation → user picks in browser → DESIGN.md extraction → Figma enrichment → Playwright baselines

The terminal state is always: invoke `writing-plans`.

#### writing-plans
**Lines:** 502 | **Trigger:** Spec exists and you need an implementation plan

Creates bite-sized implementation plans (each step 2-5 minutes) with exact file paths, complete code in every step, and TDD structure (write failing test → verify fail → implement → verify pass → commit).

**Modes:**
- **Standard tasks** (no DESIGN.md, or non-component files): TDD steps with exact commands and expected output
- **Design-aware tasks** (DESIGN.md present, component files): standard TDD plus Design Reference blocks (which DESIGN.md sections to read), inline Design Checklists (semantic tokens, typography, a11y), and a Design Verification step before commit
- **Golden samples tasks** (DESIGN.md Section 10 present, agentic products): generates fixture JSON, golden samples page with fallback renderer, and Playwright baseline capture at 3 breakpoints

Includes progressive verification: a mid-plan Design Spot-Check after component tasks and a final Design Verification as the last task.

#### executing-plans
**Lines:** 482 | **Trigger:** Plan exists and you're ready to implement

Runs implementation plans task by task.

**Modes:**
- **Subagent mode** (recommended): dispatches a fresh subagent per task with a structured micro-manifest (task description, file context, design token digest). Each task goes through three-gate review: spec compliance reviewer → code quality reviewer → design compliance reviewer (conditional on DESIGN.md). Fix iterations up to 3 attempts per gate.
- **Inline mode**: executes tasks sequentially in the current session. Review happens every 3 tasks as a batch checkpoint.

Both modes integrate with `test-driven-development`, `verification-before-completion`, and `requesting-code-review` at task boundaries.

---

### Code Review Skills

These two skills form a companion pair with an auto-chain: requesting dispatches a reviewer, and when findings return, receiving fires automatically.

#### requesting-code-review
**Lines:** 138 | **Trigger:** Completing tasks, implementing features, or before merging

The outbound side of code review. Bundles verifiable evidence, classifies risk, and dispatches an independent reviewer.

**Mandatory triggers** (all enforced, skip = No):
1. After completing a plan task in executing-plans
2. Before merge to main or any protected branch
3. After security-sensitive changes (auth, data/PII, IaC, API contracts)
4. When diff ≥200 LOC or changes touch ≥3 modules

**Evidence bundle** — every review request includes:
- What was implemented (description)
- Spec or requirements reference
- Git diff (base SHA, head SHA, scope)
- Test evidence from `verification-before-completion` (exit codes, runner output, coverage delta)
- Design compliance status (if DESIGN.md exists)
- **Redaction rule:** NO builder chain-of-thought, scratchpad, or conversation history. The reviewer sees artifacts only.

**Agent dispatch:** Dispatches `code-reviewer` agent (always) in fresh context. Adds `test-reviewer` agent when TDD context applies. Requests design-compliance review when DESIGN.md exists and the diff touches UI components. Builder and reviewer are always different contexts.

**Risk-tiered bundling:**
| Risk | Criteria | Bundle depth |
|------|----------|-------------|
| Low | ≤5 LOC, cosmetic | Diff + one-liner |
| Medium | Functional, <200 LOC | Diff + spec + test evidence |
| High | Security, data, API, ≥200 LOC, ≥3 modules | Full bundle + negative controls + audit logs |

All tiers dispatch a reviewer. The tier affects bundle depth, not whether review happens.

#### receiving-code-review
**Lines:** 188 | **Trigger:** Review feedback appears in conversation (from any source, or auto-chained from requesting)

The inbound side of code review. Processes feedback with technical rigor — no performative agreement, evidence-based pushback, severity-ordered implementation.

**6-step Response Chain** (each step has an inline rationalization trap):
1. **READ** — complete all feedback without reacting
2. **UNDERSTAND** — restate the requirement in own words
3. **VERIFY** — check against codebase reality
4. **EVALUATE** — technically sound for THIS codebase?
5. **RESPOND** — technical acknowledgment OR evidence-based pushback
6. **IMPLEMENT** — highest-severity first, test each fix individually

**Dual-path feedback handling:**
- **Structured feedback** (JSON from reviewer agent): parse → deduplicate by file:line:rule_id → sort by severity x confidence x blast_radius → process highest first
- **Prose feedback** (human reviewer): decompose into premises + conclusion → evaluate each premise independently → respond to the weakest premise

**Source-specific handling:**
- **User:** trusted, verify scope, skip to action
- **AI reviewer agent:** findings are hypotheses — verify each against codebase. Weight structural observations higher, "this doesn't work" claims lower (limited execution context).
- **External reviewer:** skeptical evaluation + YAGNI check

**Conditional routing** (after evaluating feedback):
- Design feedback + DESIGN.md exists → routes to `design-system-enforcer`
- Suspected bug meeting severity criteria → routes to `systematic-debugging`
- Test quality feedback → routes to `test-driven-development`

**Deadlock resolution:** If evidence-based pushback doesn't resolve after 2 rounds, dispatches a second-opinion agent (fresh context, receives both positions with evidence, no conversation history).

**5 AI failure modes tracked:** performative agreement, false rebuttal, scope drift, evidence-free pushback, routing avoidance. Each has a rationalization pattern and a counter-pattern.

---

### Engineering Discipline Skills

#### test-driven-development
**Lines:** 433 | **Trigger:** Implementing any feature or bug fix, before writing implementation code

Enforces RED-GREEN-REFACTOR with an Iron Law: no production code without a failing test first. If code exists before its test, delete it and start over.

**Key features:**
- RED phase gate: `test-reviewer` agent reviews the test suite before implementation begins (for task-level suites with >3 tests)
- Ecosystem-specific testing patterns per language
- Testing anti-patterns reference (in supporting file)
- Integration with `verification-before-completion` for evidence-based "tests pass" claims

#### verification-before-completion
**Lines:** 253 | **Trigger:** About to claim work is complete, fixed, passing, or ready

The most aggressive enforcement skill. Gates every completion claim on fresh verification evidence.

**Two tiers:**
- **Tier 1 (Routine claim):** "tests pass", "build succeeds", "lint clean" — requires exit code 0 from fresh process + 1-line output excerpt
- **Tier 2 (Bug-fix claim):** "I fixed X" — requires negative control (revert fix → test MUST FAIL → restore → test MUST PASS, cite both exit codes)

**5 AI failure modes covered:** in-session cache contamination, log fabrication, sandbox failure → fabricated success, prompt injection via log content, agent tool-call output deception (with read-back primitives by claim type).

**Rationalization table:** 10 rows of common excuses ("should work now", "I'm confident", "linter passed") each paired with the reality and a documented incident.

#### systematic-debugging
**Lines:** 301 | **Trigger:** Any bug, test failure, or unexpected behavior

Root-cause investigation before fixes. Four phases: Root Cause → Pattern Analysis → Hypothesis Testing → Implementation. Prevents the common AI pattern of patching symptoms without understanding cause.

**3-fix escalation rule:** If 3 attempted fixes haven't resolved the issue, stop guessing and escalate — the problem is likely architectural, not a simple bug.

#### finishing-a-development-branch
**Lines:** 394 | **Trigger:** Implementation complete, before merging, creating a PR, or removing a worktree

Pre-merge verification checklist (tests in fresh terminal, lint, type check, AI completeness scan, design compliance, diff self-consistency), then presents integration options and handles the chosen workflow.

#### using-git-worktrees
**Lines:** 331 | **Trigger:** Need parallel branch checkouts, filesystem isolation for concurrent agent work, or testing across branches

Guide to git worktrees with Claude Code's native worktree support. Covers creation, branch management, cleanup, and the mental model of shared refs + independent working trees.

---

### Design & Frontend Skills

#### design-system-enforcer
**Lines:** 328 | **Trigger:** Building web components, pages, forms, or any UI element (auto-enforced via hooks)

Enforces DESIGN.md during implementation. When DESIGN.md exists, this skill is the grounding mechanism — every component must use semantic tokens from Section 2, typography from Section 3, and component styles from Section 4.

**Key features:**
- Mandatory grounding on DESIGN.md Sections 2-4 and Section 10 (agentic products)
- Golden samples system for testing JSON render components
- Figma drift detection (capture live UI → extract tokens → compare against DESIGN.md → drift report)
- Auto-enforced via the PreToolUse hook (injects design token digest when writing component files)

#### product-redesign
**Lines:** 256 | **Trigger:** Overhauling or refreshing an existing frontend's design system

Two-phase workflow:
- **Diagnosis:** Quick scan → identify pain points → establish vision → exit gate (decide whether to proceed)
- **Treatment:** Full audit → prototype new direction → produce target DESIGN.md → migration strategy spec (token mapping, component surface, page surface, recommended paths, risks)

#### agentic-ux-patterns
**Lines:** 132 | **Trigger:** Building products with agent output, JSON render, streaming UI

Reference patterns for agentic product UX: streaming strategies (character reveal, skeleton→complete, progressive list), approval flows, error recovery, streaming accessibility, responsive agent UI, content hierarchy, thinking indicators.

---

### Workflow & Meta Skills

#### dispatching-parallel-agents
**Lines:** 209 | **Trigger:** 2+ independent tasks that can run concurrently without shared state

Decision flowchart gates on task independence before dispatching. Provides structured prompt templates with scope, constraints, and expected output format.

#### using-upp
**Lines:** 230 | **Trigger:** Auto-injected at session start via SessionStart hook

Skill discovery and routing guide. Contains the full pipeline state machine diagram, routing table for all 16 skills, red flags table, and the 1% rule: if there's even a 1% chance a skill applies, invoke it.

#### writing-skills
**Lines:** 737 | **Trigger:** Creating new skills, editing existing skills, or verifying skills work

Meta-skill for authoring other skills. TDD applied to skill development: pressure testing (RED phase without skill, GREEN phase with skill, REFACTOR if gaps), CSO (Cognitive Skill Optimization), rationalization tables, and deployment checklists.

---

## Agents

UPP ships two dedicated reviewer agents. Both operate in fresh context with no prior conversation — they evaluate artifacts only.

### code-reviewer
**Lines:** 56 | **Dispatched by:** `requesting-code-review`, `executing-plans` three-gate pipeline

Senior code reviewer with design compliance awareness. Reviews:
1. Plan alignment (implementation vs spec)
2. Code quality (error handling, type safety, naming, maintainability)
3. Architecture (SOLID, separation of concerns, integration)
4. Documentation and standards
5. Design compliance (when DESIGN.md exists): semantic token usage, typography, component patterns, accessibility baseline, Section 10 compliance for agentic products

Issues categorized as Critical (must fix), Important (should fix), or Suggestions (nice to have).

### test-reviewer
**Lines:** 119 | **Dispatched by:** `test-driven-development` RED phase gate

Reviews test suites BEFORE implementation begins. Has not seen implementation code — this is intentional. Fresh perspective catches weaknesses that the author's implementation bias would miss.

**Checks per test:**
- Trivial Pass Check: could a hardcoded return value pass this test?
- Behavior vs Implementation: is it testing what the code does or how?
- Edge case coverage
- Test isolation (no shared mutable state)

---

## Hooks

UPP ships 3 hooks that fire automatically. No configuration needed.

| Event | Matcher | What It Does |
|-------|---------|-------------|
| **SessionStart** | All events | Injects `using-upp` skill discovery + detects DESIGN.md state + caches compact token digest (colors, font, radius, shadow, registry types) |
| **PreToolUse** | Write or Edit | When writing component/page files (`src/components/**`, `app/**`, `components/**`, `pages/**`): injects cached design token digest. Skips non-component files. Deduplicated per directory. |
| **SubagentStart** | All events | Injects cached design token digest to every subagent, so even fresh-context subagents know the design system |

If no DESIGN.md exists in the project root, the design-related hook behavior silently does nothing. The hooks still handle skill discovery (SessionStart) regardless.

---

## DESIGN.md

DESIGN.md is the centerpiece of UPP's design awareness. It's an 11-section markdown file that lives in the project root, extracted from working prototypes during brainstorming.

| Section | Content |
|---------|---------|
| 1. Theme & Atmosphere | Overall aesthetic — mood, density, design philosophy |
| 2. Color Palette | Semantic tokens (primary, background, accent, muted, border) with hex values |
| 3. Typography | Font families, size hierarchy table, weights, tracking, leading |
| 4. Component Styles | Button/card/input/nav patterns: radius, padding, shadow, hover/focus states |
| 5. Layout | Spacing scale, grid/flex patterns, max-widths, whitespace philosophy |
| 6. Depth & Elevation | Shadow hierarchy, ring utilities, z-index patterns, surface layers |
| 7. Do's/Don'ts + Content Voice | Design guardrails + content patterns (buttons, errors, empty states, tooltips) |
| 8. Responsive | Breakpoint usage, responsive patterns, touch targets, collapsing strategy |
| 9. Agent Prompt Guide | Quick-reference values for AI code generation (colors, fonts, spacing) |
| 10. Agent Render System | Component registry, streaming behavior, fallback rendering — **agentic products only** |
| 11. Motion & Transitions | Timing, easing, streaming patterns, reduced-motion support |

**When DESIGN.md exists**, the entire pipeline becomes design-aware:
- Brainstorming's 6th lens fires for design & UX discovery
- Plans order tasks by design dependency and include design checklists
- Subagents receive token context via hooks
- The code-reviewer agent checks design compliance
- The design-system-enforcer skill grounds every component write

**When DESIGN.md doesn't exist**, all design features silently deactivate. The engineering discipline skills (TDD, verification, debugging, code review) work identically with or without a design system.

---

## How Skills Chain Together

UPP skills don't operate in isolation. Here's how they connect:

### The auto-chain (requesting → receiving)
When `requesting-code-review` dispatches a reviewer agent and findings return, `receiving-code-review` fires automatically. You request review once, and the full receive → triage → evaluate → implement loop follows.

### The three-gate review (inside executing-plans)
Each task in subagent mode goes through: spec-compliance reviewer → code-quality reviewer → design-compliance reviewer (if DESIGN.md). The `code-reviewer` agent handles gates 2-3.

### The verification gate (everywhere)
`verification-before-completion` fires before ANY completion claim — in `executing-plans` at task boundaries, in `finishing-a-development-branch` at merge time, in ad-hoc development before committing. It's the universal evidence gate.

### The routing network (from receiving)
When `receiving-code-review` evaluates feedback, it may route to other skills:
- Design feedback → `design-system-enforcer`
- Bug reports → `systematic-debugging`
- Test concerns → `test-driven-development`

### The TDD + test-reviewer gate
`test-driven-development` enforces writing tests first. For task-level suites (>3 tests), the `test-reviewer` agent reviews the test suite before implementation begins — fresh context, no implementation bias.

### Evidence vocabulary (shared across skills)
Three skills share identical evidence vocabulary to prevent drift:
- **Evidence** = falsifiable artifact: exit code, test runner output, git SHA, diff, coverage delta, SARIF. Self-report is the weakest tier.
- **Fresh-context reviewer** = Agent tool subagent with no prior conversation context. Receives artifacts only.
- **Risk tiers** = Low (≤5 LOC, cosmetic), Medium (functional, moderate scope), High (security, data, API, ≥200 LOC, ≥3 modules).

---

## File Structure

```
.claude-plugin/
  plugin.json                            # Plugin identity + version
  marketplace.json                       # Self-hosted marketplace catalog
hooks/
  hooks.json                             # 3 hook event registrations
  run-hook.cmd                           # Cross-platform wrapper (Unix + Windows)
  session-start                          # Skill discovery + design state detection
  pretooluse-design-inject               # Token injection on component writes
  subagent-design-bootstrap              # Token injection to subagents
skills/
  using-upp/SKILL.md                     # Skill discovery (auto-injected)
  brainstorming/SKILL.md                 # Prototype-first brainstorming
  writing-plans/SKILL.md                 # Design-aware planning
  executing-plans/                       # Unified plan execution
    SKILL.md
    implementer-prompt.md                # Subagent: task implementation
    spec-reviewer-prompt.md              # Subagent: spec compliance review
    code-quality-reviewer-prompt.md      # Subagent: code quality review
    design-compliance-reviewer-prompt.md # Subagent: design compliance review
  product-redesign/SKILL.md              # Frontend overhaul
  design-system-enforcer/SKILL.md        # DESIGN.md enforcement
  agentic-ux-patterns/SKILL.md           # Agent UI reference
  test-driven-development/               # TDD discipline
    SKILL.md
    testing-anti-patterns.md
  systematic-debugging/                  # Root cause debugging
    SKILL.md
    root-cause-tracing.md
    defense-in-depth.md
    condition-based-waiting.md
    condition-based-waiting-example.ts
    find-polluter.sh
  verification-before-completion/SKILL.md  # Evidence before claims
  requesting-code-review/SKILL.md        # Review dispatch + evidence bundling
  receiving-code-review/SKILL.md         # Review response discipline
  finishing-a-development-branch/SKILL.md # Pre-merge verification
  using-git-worktrees/SKILL.md           # Worktree management
  writing-skills/                        # Skill authoring (meta-skill)
    SKILL.md
    anthropic-best-practices.md
    testing-skills-with-subagents.md
    persuasion-principles.md
    graphviz-conventions.dot
    render-graphs.js
  dispatching-parallel-agents/SKILL.md   # Parallel subagent dispatch
agents/
  code-reviewer.md                       # Design-aware code reviewer
  test-reviewer.md                       # TDD RED phase test reviewer
scripts/
  v0-generate.mjs                        # v0 prototype generation wrapper
  package.json
```

---

## Requirements

| Requirement | What it's for | Critical? | If missing |
|-------------|--------------|-----------|------------|
| **Claude Code** | The plugin platform | **Yes** | Plugin won't load |
| **bash** | All 3 hook scripts | **Yes** | Hooks won't fire. Skills still work manually but lose automatic enforcement. macOS/Linux have it. Windows needs Git Bash or WSL. |
| **jq** | PreToolUse hook parses file paths from stdin JSON | Recommended | Design tokens won't auto-inject on component writes. Install: `brew install jq` / `apt install jq` |
| **Node.js** | v0 prototype generation during brainstorming | Optional | Brainstorming works without it — describe designs verbally. Only for prototype-first pipeline. |
| **V0_API_KEY** | v0 Platform API authentication | Optional | Same as Node.js. Set in shell profile. Requires [v0 Team plan](https://v0.dev). |
| **Figma MCP** | Design extraction + drift detection | Optional | Brainstorming skips Figma enrichment. Enforcer skips drift detection. |
| **Stitch MCP** | Mood exploration + design system generation | Optional | Brainstorming uses verbal mood description. Falls back gracefully. |

**Minimum:** Claude Code + bash. Everything else enhances but nothing blocks.

### Optional MCP setup

```bash
# Figma MCP — design extraction + drift detection
claude mcp add --scope user --transport http figma https://mcp.figma.com/mcp

# Google Stitch MCP — mood exploration + design system generation
claude mcp add --scope user --transport http stitch https://stitch.googleapis.com/mcp --header "X-Goog-Api-Key: YOUR_KEY"
```

---

## Version History

See [CHANGELOG.md](CHANGELOG.md) for the full release history.

Current version: **1.9.0** (16 skills, 2 agents, 3 hooks).

---

## License

MIT
