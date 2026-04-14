---
name: product-redesign
description: >
  Overhaul or refresh an existing frontend product's design system.
  Use when the user wants to redesign, refresh, overhaul, or modernize
  an existing frontend — full product or partial scope.
  Produces target DESIGN.md + migration strategy spec.
  Triggers on: "redesign the product", "refresh the frontend", "overhaul the UI",
  "modernize the design", "design refresh", "update the look and feel",
  "the frontend looks dated", "inconsistent design", "design debt",
  "modify the frontend design", "redo the frontend", "rethink the UX",
  or any request to systematically update an existing product's visual
  design, component system, or UX patterns.
---

# Product Redesign

You're overhauling an existing product's frontend — not building from scratch. The codebase has real users, real patterns (good and bad), and real constraints. Your job is diagnosis before treatment: understand what's broken, define where it should go, audit what exists, then produce a target design system and migration strategy.

This is not brainstorming a new feature. This is systematically transforming what exists into something better while respecting the constraints of a running product.

## The Flow

Two phases with an exit gate between them.

```
Phase 1: DIAGNOSIS
  1a. Quick scan → understand the codebase structure
  1b. Pain discovery → what's broken, why now, what scope
  1c. Vision → where should it go (mood, direction, constraints)
  
  → EXIT GATE: diagnosis summary + proceed / downscope / stop
  
Phase 2: TREATMENT
  2a. Full audit → deep token/component/page inventory
  2b. Prototypes → v0 generates the target direction
  2c. User reviews → picks direction in browser
  2d. DESIGN.md extraction → from chosen prototype
  2e. Migration strategy spec → what changes, how, what risks
  
  → Output: target DESIGN.md + migration strategy
  → Handoff to writing-plans
```

## Phase 1: Diagnosis

### 1a. Quick Scan

Before asking anything, understand what you're working with. This is a fast structural read — 2-3 minutes, not a deep audit.

**Read:**
- `package.json` — framework (Next.js/React/Vue/Svelte), major deps, version
- Route structure — `ls app/` or `ls pages/` to see what pages exist
- Component inventory — `ls src/components/` or `ls components/` — names and count, not content
- Styling approach — check for `tailwind.config.*`, CSS modules, styled-components, global CSS
- Design artifacts — check for `DESIGN.md`, design tokens directory, Figma references
- shadcn components — `ls components/ui/` or check package.json for @radix-ui deps
- Recent activity — `git log --oneline -10` to understand what's been changing

**Output to yourself (not the user):** A mental map. "This is a Next.js 16 app with 12 routes, 34 components, Tailwind CSS, 8 shadcn components, no DESIGN.md, last commit 3 days ago." This context makes your pain questions specific and relevant.

### 1b. Pain Discovery

You've scanned the codebase. Now ask about the actual problems — in context of what you found.

**Minimum 3 questions via AskUserQuestion:**

**P1: What triggered this?**

Reference what you found: "I see a [framework] app with [N] routes and [M] components using [styling approach]. What's driving the redesign?"

| Option | Description |
|--------|-------------|
| Visual debt | Inconsistent colors, fonts, spacing across pages. It grew organically and looks messy. |
| UX problems | Users struggle with specific flows — navigation confusion, hard-to-find actions, poor mobile experience |
| Brand evolution | The brand identity has changed (new logo, new colors, new voice) and the product doesn't reflect it |
| Technical modernization | Moving to new framework or component system. Design refresh is part of a larger technical upgrade |

**P2: What's the scope?**

Present the actual page/route list from your scan. "Looking at your routes: [list]. Is this a full product overhaul, or focused on specific areas?"

Let the user mark which areas are in scope. Follow-up: "What must NOT change? Any pages, flows, or components that work well and should be preserved as-is?"

**P3: Who uses this and what do they expect?**

"Who are the primary users, and how attached are they to the current design? Do they have muscle memory that a redesign would disrupt, or are they ready for something fresh?"

Ask additional questions as needed — 3 is the floor. If the user mentions specific UX problems, dig into those. If the trigger is brand evolution, ask about the new brand guidelines.

### 1c. Vision

Same Design & UX lens as prototype-first brainstorming, adapted for redesign context:

**Q1 Visual Direction:** "What visual direction should the redesigned product take?" — same options (reference product / describe mood / explore with Stitch / bring own reference). Add: "What from the CURRENT design is part of the product identity and should be preserved?"

**Q2 Information Architecture:** "Should the page structure change, or just the visual treatment? Any new pages needed, or pages to merge/remove?" For agentic products: workspace promotion question (inline vs side panel for significant output).

**Q3 Data & Agent Output** (if agentic product): Same as brainstorming — agent output types, states.

**Q4 Interaction States** (if agentic product): Same — streaming, loading, error patterns.

**Q5 Responsive & Density:** Same options. Add: "Is the current responsive behavior acceptable, or does it need to change too?"

### Exit Gate

After Phase 1, present a diagnosis summary via AskUserQuestion:

"**Diagnosis complete.** Here's what I found:
- **Product:** [framework] app, [N] routes, [M] components, [styling approach]
- **Pain:** [primary trigger] — [specific problems identified]
- **Scope:** [full product / partial — list specific pages/areas]
- **Direction:** [mood/visual direction from Q1]
- **Preserved:** [what must not change]
- **Estimated surface:** [N] pages affected, ~[M] components to update/rebuild

Ready to proceed?"

| Option | Description |
|--------|-------------|
| Proceed to Phase 2 | Full audit, prototypes, DESIGN.md, migration strategy |
| Downscope | This is smaller than a redesign — handle as regular brainstorming |
| Stop | Need more information before committing |

## Phase 2: Treatment

### 2a. Full Audit

Deep scan, now focused by the pain and vision from Phase 1. You know WHAT to look for.

**Token audit:**
- Current color palette: extract from tailwind.config + CSS custom properties + grep for hardcoded hex values in component files. Note inconsistencies (same semantic role, different values).
- Typography: font imports, `text-*` class frequency, font-weight distribution. Note: how many fonts are in use? Are they consistent?
- Spacing: most common gap/padding values. Is there a consistent scale or ad-hoc values?
- Component styles: border-radius, shadows, borders across components. Consistent or scattered?

**Component audit:**
- For each component in scope: name, line count, key props, which pages use it
- Flag inconsistencies: same component used differently across pages, duplicate patterns (two different card components doing the same thing)
- Flag debt: oversized files, components with unclear responsibility, components with hardcoded values instead of tokens

**Page audit (in-scope pages only):**
- Layout structure, which components each page uses
- Responsive behavior at current breakpoints
- UX flow through the page — entry point, primary action, secondary actions

**Output:** An audit summary you reference during migration spec writing. Key data: how many tokens change, which components need update vs rebuild vs preserve, which pages are affected.

### 2b. Prototypes

Same as greenfield prototype-first — v0 generates fresh prototypes showing the target direction.

**Stitch mood exploration** if user wants to explore options, or use their verbal direction / reference.

**v0 prompt construction** — same as greenfield but with redesign context:
- "This is a redesign of an existing [framework] app"
- "Current problems: [pain from P1]"
- "Preserve: [identity elements from Q1]"
- "New direction: [mood/visual direction]"
- Primary view, agent types, density from Q2-Q5
- Project's current tailwind.config (if exists) + installed components

Generate 2-3 variants. Full-auto adapt to project stack. Verify prototypes render before presenting.

**Async generation principle:** v0, Stitch, and Figma are async. Never treat timeouts as failures. Keep the user in the loop — share links, poll for completion, offer to proceed with verbal description if generation takes too long.

### 2c. User Reviews + Picks Direction

Same as greenfield. Dev server check → present URLs → user picks or mixes. If user wants changes, use v0 chatId for refinement.

### 2d. DESIGN.md Extraction

Same as greenfield — code-first extraction from chosen prototype. All 11 sections (or 9 for non-agentic). Figma MCP enrichment. Playwright baselines at `design-baselines/prototype/`.

Version as `v1` even if the product existed before — this is the FIRST version of the formal DESIGN.md for this product.

### 2e. Migration Strategy Spec

The unique output of this skill. Added to the spec document alongside DESIGN.md.

**Token mapping:**

```markdown
## Token Migration

| Category | Current | Target | Change Type |
|----------|---------|--------|-------------|
| [from audit] | [current value] | [from DESIGN.md] | [swap/new/remove] |
```

Map every token that changes: colors, fonts, spacing scale, border-radius, shadows. "Change Type" helps the implementation plan prioritize: swaps are low-risk (find and replace), new tokens need component updates, removed tokens need cleanup.

**Component change surface:**

```markdown
## Component Migration

| Component | Action | What Changes | Risk | Notes |
|-----------|--------|-------------|------|-------|
| [name] | Update/Rebuild/Preserve | [specific changes] | Low/Medium/High | [why] |
```

For each component in scope: what action (update tokens only, rebuild with new patterns, or preserve as-is), what specifically changes, risk level, and why.

**Page migration surface:**

```markdown
## Page Migration

| Page/Route | Scope | Components Affected | Priority | Notes |
|------------|-------|-------------------|----------|-------|
| [route] | Full/Token-only/Preserve | [list] | High/Medium/Low | [pain-driven priority] |
```

Priority is driven by pain discovery — the pages users complained about get highest priority.

**Recommended migration paths:**

Present 2-3 paths (from spec):
- **Token-first:** Update CSS vars globally → components auto-update → then rebuild individual components
- **Page-by-page:** Migrate one page at a time, highest-pain first → coexistence period
- **Component-first:** Rebuild shared components (Button, Card, Input) → then update pages to use them

Each path has tradeoffs. Don't pick one — present the options with pros/cons. The implementation plan decides.

**Risk assessment:**

```markdown
## Risks

| Risk | Impact | Mitigation |
|------|--------|-----------|
| [specific risk from audit] | [severity] | [concrete mitigation] |
```

Risks come from the audit — they're specific to THIS codebase, not generic redesign risks.

## Spec Output Format

The skill writes a spec document containing:
1. **Diagnosis summary** (from Phase 1)
2. **Target DESIGN.md** (extracted from prototype, at project root)
3. **Migration strategy** (token mapping + component surface + page surface + paths + risks)
4. **Design artifacts** (same as greenfield: DESIGN.md location, baselines, prototype reference)
5. **UX Flows** (same as greenfield: primary flow, agent interaction flow if applicable, key states)

Then handoff to writing-plans, which reads the spec and creates the incremental implementation plan.

## Anti-Slop Aesthetic Guidance

Same principles as greenfield — applied during prototype generation and DESIGN.md extraction:
- Typography: distinctive, not generic
- Color: dominant with sharp accents, not timid
- Layout: intentional composition
- Every design must feel context-specific
- For redesigns specifically: the new design should feel like an EVOLUTION, not an unrelated replacement. It should be clearly better while being recognizably the same product.
