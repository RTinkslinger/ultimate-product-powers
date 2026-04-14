---
name: writing-plans
description: >
  Write implementation plans from specs. Use when you have a spec, requirements,
  or design document and need to create an actionable plan before touching code.
  Produces design-aware plans when DESIGN.md is present: guided ordering,
  design-reference tasks, golden samples, and progressive verification.
  Falls back to standard TDD plans when no design context exists.
---

# Writing Plans

## 1. Overview

Write comprehensive implementation plans assuming the engineer has zero context for your codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume they are a skilled developer, but know almost nothing about your toolset or problem domain. Assume they don't know good test design very well.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Context:** This should be run in a dedicated worktree (created by brainstorming skill).

**Save plans to:** `docs/upp/plans/YYYY-MM-DD-<feature-name>.md`
- (User preferences for plan location override this default)

## 2. Scope Check

If the spec covers multiple independent subsystems, it should have been broken into sub-project specs during brainstorming. If it wasn't, suggest breaking this into separate plans — one per subsystem. Each plan should produce working, testable software on its own.

## 3. Design Context Detection

At plan start, check for design context. This determines whether the plan uses design-aware features or standard behavior.

1. Check the spec for a "Design Artifacts" section. If present, parse: DESIGN.md location, version, baselines path, prototype reference.
2. If the prototype reference is given as `./app/design/[chosen]/`, read `app/design/CHOSEN.md` to resolve the actual chosen prototype name.
3. Check that DESIGN.md exists at the referenced path. If no path was found in step 1, check `./DESIGN.md` (project root). If it exists, verify minimum viable content: must have at least Sections 1 (Theme), 2 (Colors), 3 (Typography), and 4 (Components). If partial, warn: "DESIGN.md is incomplete — design-aware tasks will reference only available sections." If not found anywhere, apply graceful degradation (no DESIGN.md row).
4. Extract compact token summary from DESIGN.md: the first color listed under each semantic role (background, foreground, primary, accent, muted, border), primary font family, border-radius value, shadow approach.
5. Check if DESIGN.md has Section 10. If yes, this is an agentic product — golden samples tasks will be generated.
6. Check the spec for a "UX Flows" section. If present, parse Key States (empty, loading, error, full) for golden samples fixture data.
7. Compute DESIGN.md hash for staleness tracking: `shasum -a 256 ./DESIGN.md | cut -c1-8`

**Graceful Degradation:**

| Condition | Behavior |
|-----------|----------|
| Full design (Sections 1-4+ and Section 10) | Full design awareness: ordering, design-aware tasks, golden samples, progressive verification |
| Sections 1-4+ but no Section 10 | Design awareness without golden samples (non-agentic frontend) |
| No Design Artifacts in spec, but DESIGN.md exists in project | Design Context header populated from DESIGN.md directly. Design-aware tasks used for components. Use conservatively: this DESIGN.md may not be from prototype-first and could have drift from the actual codebase. No golden samples unless Section 10 found. |
| DESIGN.md exists but is missing required sections (no Section 2, 3, or 4) | Warn: "DESIGN.md is incomplete." Fall back to standard writing-plans behavior. Do not generate design-aware tasks with references to missing sections. |
| No DESIGN.md anywhere | Standard writing-plans behavior. No Design Context header, all tasks use standard shape, no verification tasks. |

If no Design Artifacts section and no DESIGN.md: all design-aware features are OFF.

## 4. File Structure

Before defining tasks, map out which files will be created or modified and what each one is responsible for. This is where decomposition decisions get locked in.

- Design units with clear boundaries and well-defined interfaces. Each file should have one clear responsibility.
- You reason best about code you can hold in context at once, and your edits are more reliable when files are focused. Prefer smaller, focused files over large ones that do too much.
- Files that change together should live together. Split by responsibility, not by technical layer.
- In existing codebases, follow established patterns. If the codebase uses large files, don't unilaterally restructure - but if a file you're modifying has grown unwieldy, including a split in the plan is reasonable.

This structure informs the task decomposition. Each task should produce self-contained changes that make sense independently.

## 5. Task Ordering

When design context is present, frontend tasks follow dependency order:

1. **Design token setup / Tailwind configuration** — theme colors, fonts, spacing scale
2. **Shared/base components** (Button, Input, Card — the primitives)
3. **Composed components** (forms, modals, data displays — built from primitives)
4. **Page layouts and routes** (assemble composed components)
5. **Integration tasks** (API connections, data fetching)

Backend tasks slot where their frontend consumers need them. If a page needs an API endpoint, the endpoint task comes before the page task.

Non-frontend plans (pure backend, CLI tools, infrastructure) have no ordering constraint — standard writing-plans task sequencing.

## 6. Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

## 7. Plan Document Header

**Every plan MUST start with this header:**

````markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use the executing-plans skill to implement this plan task-by-task. Supports two modes: subagent-driven (recommended, fresh subagent per task with three-stage review) or inline execution. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]
````

**When DESIGN.md is present, add a Design Context block after the base header:**

````markdown
## Design Context

- **DESIGN.md:** `./DESIGN.md` (v1)
- **DESIGN.md hash:** [8-char prefix from `shasum -a 256 ./DESIGN.md | cut -c1-8`]
- **Prototype reference:** `./app/design/prototype-b/` (from CHOSEN.md) or "none"
- **Design baselines:** `./design-baselines/prototype/` or "none"
- **Key tokens:** bg: #0a0a0a, fg: #fafafa, primary: #6d28d9, accent: #22d3ee, font: Satoshi, radius: 8px, shadow: none
- **Registered JSON types:** [list from Section 10, or "none — not agentic"]
- **Key states:** empty, loading, error, complete [from UX Flows, or Section 10 vocabulary]

> Plan written against DESIGN.md v[N] (hash: [hash]). If DESIGN.md has changed
> since plan creation, the design spot-check task will flag this.

---
````

Populate every field from the detection step. Use actual values from the project's DESIGN.md and spec — no placeholders.

## 8. Task Structure — Standard

> Used for all tasks without design context, and for non-component tasks (API routes, middleware, server actions, utility hooks, configuration, backend) even when design context is present.

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

- [ ] **Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

- [ ] **Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

## 9. Task Structure — Design-Aware

A task is **design-aware** if it creates or modifies files in `src/components/`, `components/`, or component-level files in `app/` (page layouts, route components).

**NOT design-aware:** API routes, middleware, server actions, utility hooks, configuration files, tests-only changes. When in doubt, use standard.

Design-aware tasks use the standard TDD structure (Section 8) with three additions:

### Design Reference Block

Added at the top of each design-aware task, specifying which DESIGN.md sections the implementer must read:

```markdown
**Design Reference:**
- DESIGN.md Section 4 (Component Styles): border-radius, padding, shadow patterns
- DESIGN.md Section 2 (Colors): semantic color tokens
- DESIGN.md Section 10 (Agent Render): registered type and props [if applicable]
```

Select sections based on what the task touches:

| Task touches | Reference section |
|---|---|
| Colors | Section 2 |
| Typography | Section 3 |
| Component styles | Section 4 |
| Layout/spacing | Section 5 |
| Responsive | Section 8 |
| Agent render | Section 10 |

### Design Checklist

Inline in each design-aware task. Self-contained for subagents with fresh context — deliberately repeated across tasks rather than referenced from a shared location:

```markdown
**Design Checklist:**
- [ ] Uses semantic color tokens from DESIGN.md Section 2 (no hardcoded hex)
- [ ] Typography matches Section 3 hierarchy
- [ ] Component styles match Section 4 patterns (radius, padding, shadow)
- [ ] Accessible: proper semantic HTML, ARIA where needed, contrast >= 4.5:1
- [ ] Uses design-system-enforcer skill for full design grounding before implementation
```

### Design Verification Step

Final step before commit in each design-aware task:

```markdown
- [ ] **Step N: Design verification**
  Compare implementation against DESIGN.md sections in Design Reference.
  Check: semantic tokens used (no hardcoded values), patterns match Section 4,
  component renders correctly with representative data.
```

## 10. Golden Samples Tasks

Generated only when DESIGN.md has Section 10 (agentic products). Three standalone tasks inserted after the component-layer tasks.

The No Placeholders rule applies fully. The actual plan output MUST include real code blocks with project-specific content. The examples below are templates showing the shape — in the real plan, replace all example content with content derived from the project's DESIGN.md Section 10, UX Flows, and component registry.

### Task Template: Golden Samples Fixture

````markdown
### Task N: Golden Samples Fixture

**Files:**
- Create: `golden-samples.json`

- [ ] **Step 1: Create fixture file**

```json
[
  {
    "type": "AgentResponse",
    "props": {
      "content": "Here's my analysis of the quarterly data...",
      "status": "complete"
    }
  },
  {
    "type": "DataTable",
    "props": {
      "columns": ["Quarter", "Revenue", "Growth"],
      "rows": [["Q1", "$1.2M", "+12%"], ["Q2", "$1.4M", "+16%"]],
      "status": "complete"
    }
  },
  {
    "type": "AgentResponse",
    "props": { "content": null, "status": "error", "error": "Rate limit exceeded" }
  },
  {
    "type": "AgentResponse",
    "props": { "content": null, "status": "empty" }
  }
]
```

One entry per registered JSON type from DESIGN.md Section 10.
Include representative data (not lorem ipsum).
Cover states from UX Flows Key States: complete, error, empty, loading.

- [ ] **Step 2: Commit**
````

### Task Template: Golden Samples Page + Fallback Renderer

````markdown
### Task N+1: Golden Samples Page

**Files:**
- Create: `app/design/golden-samples/page.tsx`

- [ ] **Step 1: Write the failing test**

```typescript
import { render, screen } from '@testing-library/react';
import GoldenSamplesPage from './page';

test('renders all fixture types without errors', () => {
  render(<GoldenSamplesPage />);
  // Each registered type should render
  expect(screen.getByText('AgentResponse')).toBeInTheDocument();
  expect(screen.getByText('DataTable')).toBeInTheDocument();
});

test('renders fallback for unknown type', () => {
  // GenericCard shows type name + JSON
  render(<GoldenSamplesPage />);
  expect(screen.getByText('Unknown Type')).toBeInTheDocument();
});
```

- [ ] **Step 2: Run test — verify it fails**
- [ ] **Step 3: Implement golden samples page**

```tsx
import fixtures from '@/golden-samples.json';
import { componentRegistry } from '@/lib/component-registry';

function GenericCard({ type, data }: { type: string; data: unknown }) {
  return (
    <div className="rounded-lg border p-4">
      <h3 className="text-sm font-medium text-muted-foreground">{type}</h3>
      <pre className="mt-2 text-xs overflow-auto">{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}

function ErrorCard({ error }: { error: string }) {
  return (
    <div className="rounded-lg border border-destructive p-4">
      <p className="text-sm text-destructive">{error}</p>
    </div>
  );
}

function EmptyState() {
  return (
    <div className="rounded-lg border border-dashed p-8 text-center">
      <p className="text-sm text-muted-foreground">No data available</p>
    </div>
  );
}

export default function GoldenSamplesPage() {
  return (
    <div className="container mx-auto p-8 space-y-6">
      <h1 className="text-2xl font-bold">Golden Samples</h1>
      {fixtures.map((fixture, i) => {
        const Component = componentRegistry[fixture.type];
        if (!Component) return <GenericCard key={i} type={fixture.type} data={fixture.props} />;
        if (fixture.props.status === 'error') return <ErrorCard key={i} error={fixture.props.error} />;
        if (fixture.props.status === 'empty') return <EmptyState key={i} />;
        return <Component key={i} {...fixture.props} />;
      })}
    </div>
  );
}
```

- [ ] **Step 4: Run tests — verify they pass**
- [ ] **Step 5: Commit**
````

### Task Template: Golden Samples Baselines

````markdown
### Task N+2: Golden Samples Baselines

**Files:**
- Create: `design-baselines/golden-samples/` screenshots

- [ ] **Step 1: Capture baselines**

```typescript
import { test } from '@playwright/test';

test('golden samples baselines', async ({ page }) => {
  await page.goto('/design/golden-samples');
  await page.waitForLoadState('networkidle');

  for (const width of [375, 768, 1280]) {
    await page.setViewportSize({ width, height: 900 });
    await page.screenshot({
      path: `design-baselines/golden-samples/${width}px.png`,
      fullPage: true,
    });
  }
});
```

- [ ] **Step 2: Run and verify screenshots captured**

Run: `npx playwright test golden-samples-baselines`
Verify: `design-baselines/golden-samples/` contains 375px.png, 768px.png, 1280px.png

- [ ] **Step 3: Visual check — open screenshots and verify all types render**
- [ ] **Step 4: Commit baselines**
````

## 11. Progressive Design Verification

Two verification points in design-aware plans.

**Threshold:** Skip the mid-plan spot-check if the plan has fewer than 4 design-aware component tasks. Golden samples tasks do not count toward the threshold — only tasks targeting `src/components/`, `components/`, or `app/` component files. For small plans, the final verification is sufficient.

**Placement:** The mid-plan spot-check is inserted after the last task that creates/modifies a component file AND before the first page-level/integration task.

### Mid-Plan: Design Spot-Check

````markdown
### Task N: Design Spot-Check

> **Execution note:** This is a REVIEW task, not an implementation task.
> In subagent-driven-dev: the controller dispatches this as a review-only
> subagent (general-purpose agent type, NOT the implementer template).
> Do NOT run the spec-reviewer or code-quality-reviewer stages for this task.
> The spot-check IS the review.
>
> Provide the subagent with:
> - All component files created/modified in preceding tasks
> - DESIGN.md (full file)
> - The plan's Design Context header

**Verify across ALL components built so far:**
- [ ] All components use semantic tokens from DESIGN.md Section 2
  (grep for hardcoded hex values in component files — should find none)
- [ ] Typography hierarchy matches Section 3
- [ ] Component patterns match Section 4 (consistent radius, padding, shadow)
- [ ] If agentic: Section 10 registry types are all implemented
- [ ] DESIGN.md staleness check:
  Run: `shasum -a 256 ./DESIGN.md | cut -c1-8`
  Compare against plan's Design Context hash.
  If different: WARN: "DESIGN.md has changed since plan creation (was: [plan hash], now: [current hash]). Review the diff and determine if plan tasks need updating."

Report: PASS (all checks clean) or WARN (list specific violations + staleness)
````

### Final: Full Design Verification

````markdown
### Task N: Final Design Verification

- [ ] Golden samples page renders all types correctly (if agentic)
- [ ] Playwright baselines captured at 3 breakpoints
- [ ] Visual comparison: open golden-samples baselines alongside prototype baselines
  (design-baselines/golden-samples/ vs design-baselines/prototype/).
  This is a visual inspection — look for significant deviations in layout,
  color, and typography. Not a pixel-diff tool.
  If prototype baselines don't exist, skip this comparison.
- [ ] Full token comparison: tokens in built code vs DESIGN.md Sections 2, 3, 4, 5
- [ ] Accessibility: run axe-core on golden samples page, 0 violations
- [ ] DESIGN.md staleness: final hash check (same as spot-check)
````

## 12. No Placeholders

Every step must contain the actual content an engineer needs. These are **plan failures** — never write them:
- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above" (without actual test code)
- "Similar to Task N" (repeat the code — the engineer may be reading tasks out of order)
- Steps that describe what to do without showing how (code blocks required for code steps)
- References to types, functions, or methods not defined in any task

This applies to ALL tasks — including golden samples tasks. The fixture JSON, page component code, fallback renderers, and Playwright tests must all be written out in full with project-specific content.

## 13. Remember

- Exact file paths always
- Complete code in every step — if a step changes code, show the code
- Exact commands with expected output
- DRY, YAGNI, TDD, frequent commits

## 14. Self-Review

After writing the complete plan, look at the spec with fresh eyes and check the plan against it. This is a checklist you run yourself — not a subagent dispatch.

**1. Spec coverage:** Skim each section/requirement in the spec. Can you point to a task that implements it? List any gaps.

**2. Placeholder scan:** Search your plan for red flags — any of the patterns from the "No Placeholders" section above. Fix them.

**3. Type consistency:** Do the types, method signatures, and property names you used in later tasks match what you defined in earlier tasks? A function called `clearLayers()` in Task 3 but `clearFullLayers()` in Task 7 is a bug.

**Design-aware checks (if Design Context present):**

**4. Ordering:** Are frontend tasks in dependency order (tokens -> shared -> composed -> pages)?

**5. Design references:** Does every design-aware task specify which DESIGN.md sections to read? Are the sections correct for what the task does?

**6. Verification coverage:** Is there a mid-plan spot-check after component tasks (if >= 4 design-aware tasks) AND a final verification as the last task?

If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a spec requirement with no task, add the task.

## 15. Execution Handoff

**"Plan complete and saved to `docs/upp/plans/<filename>.md`.**

**Execute with:** the executing-plans skill

The skill supports two modes:
- **Subagent mode** (recommended) — fresh subagent per task, three-stage review (spec → quality → design)
- **Inline mode** — execute in this session with checkpoints

Which mode would you like? (Default: subagent mode)

You can override at any time: "use inline" or "use subagents"

**Design verification note:** The mid-plan "Design Spot-Check" task is a review task, not an implementation task. In subagent mode:
- Dispatch as a general-purpose review subagent (NOT implementer template)
- Skip the spec-reviewer and code-quality-reviewer stages
- The spot-check IS the review — it reports PASS or WARN
