# Ultimate Product Powers (UPP)

**Design-aware product development skills for Claude Code.**

UPP is a comprehensive Claude Code plugin that covers the full product development lifecycle — from brainstorming ideas into designs, through implementation planning, to multi-agent execution with three-gate code review. Every skill is deeply researched, stress-tested through real usage, and tuned for product-oriented work.

What makes UPP different: design is a first-class concern throughout the pipeline. When you build frontends, UPP's prototype-first brainstorming generates working prototypes and extracts a DESIGN.md. That DESIGN.md then flows through every subsequent skill — plans are ordered by design dependencies, subagents receive design tokens in their context, and a dedicated design compliance reviewer catches drift.

---

## Installation

```bash
/plugin marketplace add RTinkslinger/ultimate-product-powers
/plugin install upp@ultimate-product-powers
```

That's it. All 14 skills, 3 hooks, and the code-reviewer agent are immediately available.

### Optional: Prototype Generation Setup

For the brainstorming skill's prototype-first pipeline (Stitch mood boards → v0 prototypes → DESIGN.md extraction):

**v0 API key:** Set `V0_API_KEY` in your shell profile (`~/.zshrc` or `~/.bashrc`). Requires a [v0 Team plan](https://v0.dev). The v0-sdk dependency is vendored — no `npm install` needed.

**MCP integrations (optional, enhance brainstorming):**
```bash
# Figma MCP — design extraction + drift detection
claude mcp add --scope user --transport http figma https://mcp.figma.com/mcp

# Google Stitch MCP — mood exploration + design system generation
claude mcp add --scope user --transport http stitch https://stitch.googleapis.com/mcp --header "X-Goog-Api-Key: YOUR_KEY"
```

---

## The Pipeline

UPP provides a complete brainstorm-to-build pipeline:

```
Idea → Brainstorming → Spec + DESIGN.md → Writing-Plans → Plan → Executing-Plans → Ship
         │                    │                  │                    │
         ├─ Prototype-first   ├─ Design tokens   ├─ Bottom-up order  ├─ Micro-manifest context
         ├─ 5-lens discovery  ├─ UX flows         ├─ Design-aware     ├─ Three-gate review
         └─ Stitch + v0       └─ Golden samples   │  task shapes      ├─ Fix iterations (max 3)
                                                   └─ Verification    └─ Design compliance
```

### How It Works

1. **Brainstorming** explores the problem space through 5 discovery lenses, generates working prototypes via v0 + Stitch, extracts DESIGN.md from the chosen prototype, and produces a design spec.

2. **Writing-plans** reads the spec and creates a design-aware implementation plan — tasks ordered by design dependency (tokens → shared components → composed components → pages), with design reference blocks, inline design checklists, golden samples tasks for agentic products, and progressive verification.

3. **Executing-plans** dispatches a fresh subagent per task with structured micro-manifest context. Each task goes through a three-gate review pipeline: spec compliance → code quality → design compliance (conditional). A dedicated design spot-check runs mid-plan, and a final design verification closes the loop.

4. **Three hooks** enforce design tokens automatically at every step — SessionStart detects DESIGN.md and caches a token digest, PreToolUse injects the digest when writing component files, SubagentStart bootstraps every subagent with design context.

---

## Skills

### Core Pipeline

| Skill | Lines | Purpose |
|-------|-------|---------|
| **brainstorming** | 543 | Turn ideas into designs + specs. Prototype-first for greenfield frontend (Stitch mood exploration → v0 prototypes → DESIGN.md extraction). 5-lens + Design & UX discovery. |
| **writing-plans** | 502 | Create implementation plans from specs. Design-aware ordering (tokens → components → pages), design-aware task shapes, golden samples tasks, progressive verification. |
| **executing-plans** | 481 | Unified plan execution — subagent mode (fresh subagent per task, micro-manifest context, three-gate review) or inline mode. Handles design spot-checks and final verification. |

### Design & Frontend

| Skill | Lines | Purpose |
|-------|-------|---------|
| **design-system-enforcer** | 328 | Enforce DESIGN.md during implementation. Mandatory grounding on Sections 2-4 and 10. Golden samples, Figma drift detection. Auto-enforced via hooks. |
| **product-redesign** | 256 | Overhaul existing frontend design systems. Two-phase: Diagnosis (scan → pain → vision → exit gate) then Treatment (audit → prototypes → DESIGN.md → migration strategy). |
| **agentic-ux-patterns** | 132 | Reference patterns for agent UI — streaming strategies, approval flows, error recovery, streaming accessibility, responsive agent UI, content hierarchy, thinking indicators. |

### Engineering Discipline

| Skill | Lines | Purpose |
|-------|-------|---------|
| **test-driven-development** | 371 | TDD discipline enforcement. Red-Green-Refactor with Iron Law: no production code without a failing test first. Code before test? Delete it. Start over. |
| **systematic-debugging** | 296 | Root cause investigation before fixes. Four phases: Root Cause → Pattern Analysis → Hypothesis Testing → Implementation. 3-fix escalation rule. |
| **verification-before-completion** | 139 | Evidence before claims. No completion claims without fresh verification output. Catches "should work now" and "looks correct." |

### Code Review

| Skill | Lines | Purpose |
|-------|-------|---------|
| **requesting-code-review** | 104 | When and how to request review — mandatory triggers, SHA collection, code-reviewer agent dispatch, acting on feedback. |
| **receiving-code-review** | 213 | How to handle review feedback with technical rigor. No performative agreement ("Great point!"). Verify before implementing. Push back when reviewer is wrong. |

### Meta

| Skill | Lines | Purpose |
|-------|-------|---------|
| **writing-skills** | 737 | TDD applied to skill authoring. Skill assessment (process vs expertise), CSO, pressure testing, rationalization tables, graphviz conventions. Synthesized from superpowers + SKILL-CRAFT. |
| **dispatching-parallel-agents** | 182 | Dispatch subagents for independent parallel work. Decision flowchart gates on task independence. Focused prompts with scope, constraints, expected output. |
| **using-upp** | 129 | Skill discovery guide — auto-injected at session start. 1% rule, routing table for all 13 skills, red flags table, design awareness trigger. |

---

## Hooks

UPP ships three hooks that fire automatically when the plugin is enabled:

| Event | Matcher | What It Does |
|-------|---------|-------------|
| **SessionStart** | All events | Injects using-upp skill discovery mandate + detects DESIGN.md state + caches token digest |
| **PreToolUse** | Write\|Edit | Injects cached design token digest when writing component/page files |
| **SubagentStart** | All events | Injects cached design token digest to every subagent |

No configuration needed. The hooks read DESIGN.md from the project root, extract a compact token digest (colors, font, radius, shadow, registry types), and inject it at the right moments. If no DESIGN.md exists, the hooks silently do nothing.

---

## Agent

**code-reviewer** — Senior code reviewer with design compliance awareness. Reviews plan alignment, code quality, architecture, documentation, and — when DESIGN.md exists — checks semantic token usage, typography, component patterns, accessibility baseline, and Section 10 compliance for agentic products.

---

## DESIGN.md

DESIGN.md is the centerpiece of UPP's design enforcement. It's an 11-section markdown file extracted from working prototypes during brainstorming:

1. Theme & Atmosphere
2. Color Palette (semantic tokens)
3. Typography (hierarchy table)
4. Component Styles (radius, padding, shadow)
5. Layout (spacing scale, grid patterns)
6. Depth & Elevation (shadows, z-index)
7. Do's/Don'ts + Content Voice
8. Responsive (breakpoints, touch targets)
9. Agent Prompt Guide
10. Agent Render System (component registry, streaming, fallback) — agentic products only
11. Motion & Transitions

When DESIGN.md exists, the entire pipeline becomes design-aware: plans order tasks by design dependency, subagents receive token context, and the design compliance reviewer verifies every component against the spec.

---

## File Structure

```
.claude-plugin/
  plugin.json                          # Plugin identity
  marketplace.json                     # Self-hosted marketplace catalog
hooks/
  hooks.json                           # 3 hook event registrations
  run-hook.cmd                         # Cross-platform wrapper (Unix + Windows)
  session-start                        # Skill discovery + design state detection
  pretooluse-design-inject             # Token injection on component writes
  subagent-design-bootstrap            # Token injection to subagents
skills/
  using-upp/SKILL.md                   # Skill discovery (auto-injected)
  brainstorming/SKILL.md               # Prototype-first brainstorming
  writing-plans/SKILL.md               # Design-aware planning
  executing-plans/                     # Unified execution
    SKILL.md
    implementer-prompt.md              # Subagent: task implementation
    spec-reviewer-prompt.md            # Subagent: spec compliance review
    code-quality-reviewer-prompt.md    # Subagent: code quality review
    design-compliance-reviewer-prompt.md  # Subagent: design compliance review
  product-redesign/SKILL.md            # Frontend overhaul
  design-system-enforcer/SKILL.md      # DESIGN.md enforcement
  agentic-ux-patterns/SKILL.md         # Agent UI reference
  test-driven-development/             # TDD discipline
    SKILL.md
    testing-anti-patterns.md
  systematic-debugging/                # Root cause debugging
    SKILL.md
    root-cause-tracing.md
    defense-in-depth.md
    condition-based-waiting.md
    condition-based-waiting-example.ts
    find-polluter.sh
  verification-before-completion/SKILL.md  # Evidence before claims
  requesting-code-review/SKILL.md      # Review dispatch
  receiving-code-review/SKILL.md       # Review response discipline
  writing-skills/                      # Skill authoring (TDD + SKILL-CRAFT)
    SKILL.md
    anthropic-best-practices.md
    testing-skills-with-subagents.md
    persuasion-principles.md
    graphviz-conventions.dot
    render-graphs.js
  dispatching-parallel-agents/SKILL.md # Parallel subagent dispatch
agents/
  code-reviewer.md                     # Design-aware code reviewer
scripts/
  v0-generate.mjs                      # v0 prototype generation wrapper
  package.json
README.md
```

---

## Requirements

- **Claude Code** (Claude Code only — no Cursor/Copilot/Gemini support)
- **bash** (for hooks)
- **jq** (for PreToolUse hook — exits silently if missing)
- **Node.js + npm** (only for v0 prototype generation in brainstorming)

---

## License

MIT
