---
name: executing-plans
description: Unified plan execution skill — merges executing-plans and subagent-driven-development into one skill with two modes (subagent-driven and inline). Design-aware execution with three-gate review pipeline (spec, quality, design). Graceful fallback to standard two-gate behavior when no design context is present.
---

# Executing Plans

## 1. Overview

Execute implementation plans by dispatching work and reviewing results. Two modes, one skill.

**Subagent mode** (recommended for plans with 4+ tasks or design context): Dispatch a fresh subagent per task with micro-manifest context packaging. Each completed task passes through a three-stage review pipeline: spec compliance, code quality, then design compliance (when the task is design-aware). Tasks marked as `REVIEW task` get custom dispatch as review-only subagents. A final holistic code review catches cross-task issues after all tasks complete.

**Inline mode** (for simple plans or when subagents are not available): Execute tasks sequentially in the current session with checkpoints after each task. Design checklists are verified inline. No subagent dispatch.

This is the unified execution skill — it handles both subagent-driven and inline plan execution in a single skill.

**Announce at start:** "I'm using the executing-plans skill to implement this plan." Then state the mode:
- "Using subagent mode -- fresh subagent per task with three-stage review."
- "Using inline mode -- executing in this session with checkpoints."

---

## 2. Workspace Setup

Before starting execution, ensure an isolated workspace exists.

**If a git worktree was set up by brainstorming:** Work in that worktree. Verify it's current with main.

**If on a feature branch:** Confirm you are NOT on main/master. If you are, stop and create a branch.

**If neither:** Create a feature branch before proceeding:
```bash
git checkout -b feat/<feature-name>
```
Do not start implementation on main/master without explicit user consent.

**For parallel-safe execution** (optional): Set up a git worktree for full isolation:
```bash
git worktree add ../worktree-<feature> -b feat/<feature-name>
cd ../worktree-<feature>
```
Worktrees let you keep main clean and run the dev server from the worktree. Clean up after merge: `git worktree remove ../worktree-<feature>`.

---

## 3. Mode Selection

**Default behavior:**
- If subagents are available (Claude Code, Codex, or any platform with Agent/Task tool): **use subagent mode**
- If subagents are not available: **use inline mode**
- User can override: "use inline" or "use subagents"

**Recommendation to user:** "Subagent mode is strongly recommended for plans with design context or 4+ tasks. Fresh context per task prevents quality degradation over long execution sequences."

**Why subagents:** You delegate tasks to specialized agents with isolated context. By precisely crafting their instructions and context, you ensure they stay focused and succeed at their task. They never inherit your session's context or history -- you construct exactly what they need. This also preserves your own context for coordination work.

---

## 4. Loading the Plan

Read the plan file once. Extract everything upfront -- do NOT make subagents read the plan file.

**Step 1:** Read plan file. Extract ALL tasks with their full text, including:
- Step details and substeps
- `**Design Reference:**` blocks
- `**Design Checklist:**` blocks
- Files lists
- Code blocks with interfaces and type signatures

**Step 2:** Detect design context. Does the plan have a `## Design Context` header?
- **If yes:** Note the DESIGN.md path, hash, key tokens (colors, fonts, radius, shadow), registered JSON types. All design-aware features are ON.
- **If no:** All design-aware features are OFF. The skill operates as standard two-gate execution (spec + quality only). No design gates, no design spot-checks, no final design verification.

**Step 3:** For each task, determine if it is design-aware: check for a `**Design Reference:**` block in the task text. Mark design-aware tasks for three-gate review; mark others for two-gate review.

**Step 4:** Create task tracking list with all tasks, their design-awareness status, and completion state.

**Step 5:** Identify special tasks:
- **Design Spot-Check:** Tasks with the `> **Execution note:** This is a REVIEW task, not an implementation task.` marker
- **Final Design Verification:** The last task containing a verification checklist (typically the final task in a design-aware plan)

**Step 6:** Review the plan critically before starting. Identify any questions or concerns about the approach, missing dependencies, or gaps that would prevent completing the work. If concerns exist, raise them with the human before proceeding. Only begin dispatch/execution after concerns are resolved.

**When to revisit the plan mid-execution:** If conditions change during execution — the human updates the plan, a fundamental approach proves wrong, or a blocker reveals the plan itself is flawed — stop. Return to Step 1 to re-extract and re-assess. Don't force through blockers by guessing.

---

## 5. When NOT to Delegate

Even in subagent mode, some tasks should be executed by the controller directly:

**Creative/exploratory work** -- Tasks with unclear outcomes where the controller's holistic context across the full plan is essential. If the task says "figure out the best approach" rather than "implement X," keep it.

**Tightly coupled with previous task** -- Shares mutable state or depends on uncommitted changes from the previous task. If the prior task's output isn't committed yet, the subagent won't see it.

**Trivially small** -- Fewer than 5 lines of change. The overhead of constructing a micro-manifest, dispatching, and reviewing exceeds the value of delegation.

**Interactive debugging** -- Requires iterating across multiple files with rapid feedback loops. Subagents lack the iterative context needed for effective debugging.

When staying monolithic, execute the task inline (as if in inline mode), then resume subagent dispatch for subsequent tasks.

---

## 6. Micro-Manifest Context Packaging

When dispatching an implementer subagent, construct a micro-manifest -- a structured prompt assembled from the plan task. This replaces the raw "Task Description + Context" pattern. The structure ensures the subagent receives typed contracts, verifiable criteria, and design constraints upfront.

```
## Micro-Manifest

### Task
[Full task description from plan -- including all steps, substeps, and details.
Do NOT summarize. Paste the complete task text.]

### Files
[Exact file paths from the task's Files block.
Include whether each file is CREATE or MODIFY.]

### Interface Contracts
[Type signatures, prop interfaces, function signatures relevant to this task.
Extract from the plan's code blocks -- TypeScript interfaces, prop types, return types.
If the plan doesn't specify interfaces, extract from existing code in the target files.
These contracts are what the spec reviewer will verify against.]

### Acceptance Criteria
[Test names and expected behavior from the plan's test steps.
Include both unit test expectations and integration verification steps.]

### Architectural Context
[1-3 sentences: where this task fits in the feature, what was built before it,
what depends on it next. The subagent needs to understand the bigger picture
without reading the entire plan.]

### Design Context (if design-aware task)
[From plan's Design Reference block -- specific DESIGN.md sections to read.
 Example: "Read DESIGN.md Sections 2 (Colors), 3 (Typography), 4 (Components)"]
[From plan's Design Context header -- key tokens for quick reference.
 Example: "Primary: oklch(0.65 0.24 265), Font: 'Instrument Sans', Radius: 0.75rem"]
NOTE: This is upfront awareness. If Layer 2 hooks inject different tokens at write
time (because DESIGN.md changed since plan creation), the hook injection takes
precedence.

### Design Checklist (if design-aware task)
[From plan's Design Checklist block -- inline, self-contained.
 Example:
 - [ ] All colors use CSS variables or Tailwind semantic classes
 - [ ] Typography matches Section 3 hierarchy
 - [ ] Border-radius uses design token, not arbitrary value
 - [ ] Semantic HTML (button not div with onClick)
 - [ ] Color contrast >= 4.5:1 for text]

### Forbidden Patterns
[From design checklist: "no hardcoded hex values", "no arbitrary Tailwind values", etc.]
[From plan constraints: "do not modify components/ui/ directory", "do not add new
dependencies without approval", etc.]
[Each pattern as a bullet point. These are negative constraints the implementer must
not violate.]
```

The micro-manifest adds over raw text paste: **Interface Contracts** (type safety -- the spec reviewer verifies conformance), **Acceptance Criteria** (verifiable -- not just "it works"), **Design Context** (targeted sections with precedence rule for hook injection), and **Forbidden Patterns** (negative constraints that prevent common violations).

---

## 7. Dispatch & Execution Loop

For each task in the tracking list:

**1. Construct micro-manifest** from the task text + plan context (Section 6).

**2. Dispatch implementer subagent** using the `./implementer-prompt.md` template with the micro-manifest pasted inline. Do NOT make the subagent read the plan file.

**3. Handle implementer status** (see Section 10 for each status).

**4. If DONE or DONE_WITH_CONCERNS**, run the review pipeline:

> **a. Gate 1 -- Spec Compliance:** Dispatch spec-compliance reviewer using `./spec-reviewer-prompt.md`. Provide the full task requirements, interface contracts from the micro-manifest, and the implementer's report.
>
> If the reviewer finds issues: dispatch a fix subagent (see Section 9). Maximum 3 fix cycles per gate. If the issue persists after 3 attempts, escalate to the human.
>
> **b. Gate 2 -- Code Quality:** Dispatch code-quality reviewer using `./code-quality-reviewer-prompt.md`. Provide the implementer's report, plan requirements, and git SHAs (base and head).
>
> If the reviewer finds issues: dispatch a fix subagent. Maximum 3 fix cycles. Then escalate.
>
> **c. Gate 3 -- Design Compliance (only for design-aware tasks):** Dispatch design-compliance reviewer using `./design-compliance-reviewer-prompt.md`. Provide the Design Reference, Design Checklist, relevant DESIGN.md sections, and the implementer's report including their design self-assessment.
>
> If the reviewer finds issues: dispatch a fix subagent. Maximum 3 fix cycles. Then escalate.

**5. Mark task complete** in the tracking list.

**6. Next task** -- or handle spot-check/final verification if the next item is a special task (Section 12 or Section 14).

### NEVER

- **Skip any review stage.** Every completed task goes through all applicable gates.
- **Start code quality review before spec compliance passes.** Gates are sequential. Spec first, quality second, design third.
- **Start design compliance review before code quality passes.** The three gates are ordered. No shortcuts.
- **Move to next task with unfixed issues.** If a reviewer found problems and the fix cycles haven't resolved them, escalate -- don't proceed.
- **Dispatch multiple implementer subagents in parallel.** Sequential execution prevents file conflicts. One task at a time.

---

## 8. Three-Gate Review Pipeline

| Gate | Purpose | Template | Runs When |
|------|---------|----------|-----------|
| 1. Spec Compliance | Did the agent build what was asked? Nothing more, nothing less. | `./spec-reviewer-prompt.md` | Always |
| 2. Code Quality | Is it well-built? Clean, tested, maintainable. | `./code-quality-reviewer-prompt.md` | Always |
| 3. Design Compliance | Does it match DESIGN.md constraints? Tokens, typography, patterns, a11y. | `./design-compliance-reviewer-prompt.md` | Only for design-aware tasks |

**Design compliance is conditional.** It fires only when the task text contains a `**Design Reference:**` block. For non-design tasks (backend logic, infrastructure, configuration, data models), the pipeline is two-stage (spec + quality) -- standard two-stage only (spec + quality).

**Reviewer independence.** Each reviewer is a fresh subagent with no knowledge of prior reviewers' findings. They receive only the task requirements and the implementation code. This prevents reviewers from rubber-stamping prior approvals.

**Gate ordering matters.** Spec compliance ensures the right thing was built before quality checks whether it was built well. Design compliance verifies visual/interaction fidelity only after structural correctness is confirmed. Reviewing design on code that doesn't match spec is wasted effort.

---

## 9. Fix Iterations

When a reviewer finds issues, the controller dispatches a NEW implementer subagent with a targeted fix manifest:

```
## Fix Manifest

### Original Task
[Brief: which task this fixes, one sentence]

### Issues Found
[From reviewer report -- specific issues with file:line references.
Paste the reviewer's findings verbatim. Do not paraphrase.]

### Files to Fix
[Only the files with issues, not the full task file list]

### What Passed
[What the reviewer approved -- do NOT change these parts.
The fix subagent must preserve everything that already passed review.]
```

The fix subagent uses the same `./implementer-prompt.md` template, with the fix manifest replacing the micro-manifest. After the fix, the SAME reviewer type re-reviews (re-dispatch a fresh reviewer subagent with the updated code).

**Fix cycle flow:**
1. Reviewer finds issues and reports them
2. Controller constructs fix manifest from reviewer report
3. Controller dispatches new implementer subagent with fix manifest
4. Implementer applies fixes, reports back
5. Controller re-dispatches reviewer (fresh subagent) to re-review
6. If issues remain: repeat from step 2
7. If approved: proceed to next gate

**Termination:** Maximum 3 fix cycles per review gate. If the issue persists after 3 attempts:
- Present the reviewer's findings to the human
- Ask for guidance: "The implementer hasn't resolved [specific issue] after 3 attempts. Should I try a different approach, use a more capable model, or do you want to fix this manually?"
- Do NOT proceed to the next gate or the next task until the human responds

---

## 10. Handling Implementer Status

Implementer subagents report one of four statuses. Handle each appropriately:

**DONE:** Proceed to the review pipeline (Section 7, step 4).

**DONE_WITH_CONCERNS:** The implementer completed the work but flagged doubts. Read the concerns before proceeding:
- If concerns are about **correctness or scope** -- address them before entering review. The concern may indicate a spec misunderstanding that review would catch anyway, but it's faster to resolve now.
- If concerns are **observations** (e.g., "this file is getting large", "I noticed a potential optimization") -- note them and proceed to review.

**NEEDS_CONTEXT:** The implementer needs information that wasn't provided. Provide the missing context and re-dispatch. Common causes: missing type definitions, unclear dependency relationships, ambiguous acceptance criteria. Before re-dispatching, verify the information gap isn't a plan deficiency -- if the plan itself is missing critical detail, flag it to the human.

**BLOCKED:** The implementer cannot complete the task. Assess the blocker:
1. **Context problem** -- provide more context and re-dispatch with the same model
2. **Needs more reasoning** -- re-dispatch with a more capable model
3. **Task too large** -- break it into smaller pieces and dispatch sequentially
4. **Plan is wrong** -- escalate to the human. The plan may have incorrect assumptions.

**Never** ignore an escalation or force the same model to retry without changes. If the implementer said it's stuck, something needs to change.

---

## 11. Model Selection

Route tasks to the least powerful model that can handle them. Well-specified tasks don't need the most capable model. Under-powered models on judgment-heavy tasks waste fix iterations.

| Task Signal | Model Tier | Rationale |
|------------|-----------|-----------|
| Touches 1-2 files, complete spec, no judgment calls | Fast (haiku/sonnet) | Mechanical execution -- clear inputs, clear outputs |
| Single-file component with `**Design Reference:**` block | Standard (sonnet) minimum | Design judgment cannot be mechanical. Tokens, typography, accessibility require understanding intent, not just following rules |
| Touches multiple files, integration concerns | Standard (sonnet) | Needs coordination across file boundaries |
| Architecture decisions, design judgment, review tasks | Capable (opus) | Needs deep reasoning about tradeoffs |
| Design Spot-Check, Final Design Verification | Capable (opus) | Holistic design assessment across multiple components |
| Fix iterations (reviewer-triggered) | Same tier as original task | Consistency with the original implementation context |

**When in doubt, go one tier up.** A slightly overpowered model wastes a small amount of compute. An underpowered model wastes fix iterations, reviewer cycles, and human escalations.

---

## 12. Design Spot-Check Dispatch

When the controller encounters a task with the marker:

```
> **Execution note:** This is a REVIEW task, not an implementation task.
```

Handle it differently from implementation tasks:

**1. Do NOT use the `./implementer-prompt.md` template.** This task has no files to create, no tests to write, no code to implement.

**2. Dispatch as a general-purpose review subagent** with the task's full text as the prompt. The task text already contains the complete review checklist -- paste it verbatim.

**3. Provide the subagent with:**
- All component files created or modified in preceding tasks
- DESIGN.md (full file, not just sections -- the spot-check needs holistic view)
- Plan's Design Context header (key tokens, hash)

**4. Do NOT run the three-gate review pipeline.** The spot-check IS the review. Running spec/quality/design reviewers on a review task is nonsensical.

**5. Expect a PASS or WARN report:**
- **PASS:** Continue to the next task.
- **WARN:** Present the spot-check findings to the human before proceeding. The human decides whether to fix now or defer.

---

## 13. Inline Execution

When executing without subagents (inline mode), the controller does all work directly.

**1. Load plan** -- same as Section 4. Extract all tasks, detect design context, identify special tasks.

**2. For each task:**

> a. Follow each step exactly. The plan has bite-sized steps -- execute them as written.
>
> b. Run verifications as specified in the plan. If a step says "run tests," run them. If it says "verify the component renders," verify it.
>
> c. **If design-aware task:** After implementation, check every item in the task's Design Checklist. Verify each one (read the actual code, don't assume). If any item fails, fix it before moving on.
>
> d. **Commit** after each logical step -- not just at the end of the task. Each commit should be independently revertible.
>
> e. **Checkpoint:** Summarize what was done, mark task complete. State: "Task N complete. [1-sentence summary]. Moving to Task N+1."

**3. Spot-check tasks:** Execute the spot-check task's full checklist exactly as written in the plan. Do NOT partially reimplement or skip items -- the plan specifies every verification item. Run each check, note results.

**4. Final verification:** Execute the final verification task's full checklist as written in the plan (see Section 14 for the standard items).

**5. When blocked:** Stop and ask for help. Do not guess, do not skip the step, do not improvise a workaround. State what you're blocked on and what you need.

---

## 14. Final Design Verification

Always the last substantive task in a design-aware plan. Execute it in whatever mode is active.

**Subagent mode:** Dispatch as a review subagent using the same pattern as spot-check dispatch (Section 12). Provide all component files, DESIGN.md, and plan's Design Context header. Do NOT run the three-gate pipeline -- this is a review task.

**Inline mode:** Run the checklist inline, verifying each item by reading code and running tools.

**Standard verification items** (from plan -- execute all that apply):

1. **Golden samples page** renders all registered JSON types correctly (if agentic product with Section 10)
2. **Playwright baselines** captured at 3 breakpoints (mobile, tablet, desktop) and stored in `design-baselines/golden-samples/`
3. **Visual comparison:** Golden-samples baselines vs prototype baselines -- visual inspection for alignment, not pixel-diff (reasonable variation is expected between prototype and production)
4. **Full token comparison:** Code vs DESIGN.md Sections 2 (colors), 3 (typography), 4 (components), 5 (spacing/layout). Every token in DESIGN.md should map to usage in code. Flag unused tokens and unmatched code values.
5. **Accessibility:** Run axe-core on the golden samples page. Zero critical or serious violations. Note moderate/minor for human review.
6. **DESIGN.md staleness:** Compare current DESIGN.md hash against the hash recorded in the plan's Design Context header. If they differ, DESIGN.md was modified during implementation -- verify the changes are intentional and reflected in the code.

**If no design context exists:** Skip this section entirely. Non-design plans have no final design verification.

---

## 15. Final Holistic Code Review

**Subagent mode only.** After all tasks are complete and individually reviewed, dispatch a final code-quality reviewer subagent that reviews the ENTIRE implementation holistically.

**Scope:** The full diff from the plan's starting commit to the current HEAD. Not per-task -- the entire feature branch diff.

**What it catches that per-task reviews cannot:**

- **Cross-task consistency:** Naming conventions that drifted between tasks (Task 1 uses `handleSubmit`, Task 4 uses `onFormSubmit` for the same pattern). Duplicate utility functions created independently in different tasks.
- **Dead code from fix iterations:** Fix subagents sometimes leave dead imports, unused variables, or commented-out code from previous attempts.
- **Integration issues:** Components built independently in separate tasks that don't compose correctly. Props that don't match across boundaries. State that doesn't flow as expected.
- **Architectural coherence:** The feature as a whole should read as if one developer built it, not as five isolated patches.

**Dispatch:** Use the same `./code-quality-reviewer-prompt.md` template, but scope it to the full diff:
- `BASE_SHA`: Commit before the first task started
- `HEAD_SHA`: Current commit (after all tasks complete)
- `WHAT_WAS_IMPLEMENTED`: Brief summary of the entire plan (all tasks, not just one)

**If the holistic reviewer finds issues:** Fix them inline (the controller handles this directly -- don't dispatch subagents for cross-task fixes that require holistic context). Commit fixes. Do NOT re-run the holistic review unless changes were substantial.

**Inline mode:** No holistic review. The controller already has full context from executing every task in sequence -- cross-task issues are visible during execution.

---

## 16. Finishing

After all tasks complete, design verification passes (if applicable), and holistic review is resolved:

1. **Verify all tests pass:**
   ```bash
   npm test  # or the project's test command
   ```
   If any tests fail, fix them before proceeding. Do not ship broken tests.

2. **Verify the build succeeds:**
   ```bash
   npm run build  # or the project's build command
   ```

3. **Review the full diff:**
   ```bash
   git diff main..HEAD --stat  # summary of all changes
   git diff main..HEAD          # full diff for review
   ```

4. **Present options to the user:**
   - **Merge to main:** `git checkout main && git merge <branch> && git branch -d <branch>`
   - **Create a PR:** `gh pr create --title "<title>" --body "<summary>"`
   - **Keep working:** Stay on branch, continue in a follow-up session
   - **Cleanup worktree** (if used): `git worktree remove ../worktree-<feature>`

5. **Execute the user's choice.** Do not merge or create PRs without explicit user consent.

---

## Graceful Degradation Summary

| Condition | Behavior |
|-----------|----------|
| Plan has Design Context + subagents available | Full: subagent mode, micro-manifest with design fields, three-gate review (spec + quality + design), spot-check dispatch, final design verification, holistic review |
| Plan has Design Context + no subagents | Inline mode with design checkpoints (Design Checklist verification after each design-aware task), spot-check inline, final design verification inline |
| Plan has no Design Context + subagents | Subagent mode, two-gate review (spec + quality), no design gates, no spot-check, no design verification, holistic review |
| Plan has no Design Context + no subagents | Inline mode with basic checkpoints. Standard step-by-step execution. |

---

## Prompt Templates

All prompt templates live alongside this skill file:

- `./implementer-prompt.md` -- Dispatch implementer subagent (micro-manifest structure, design checklist, commit-per-step, forbidden patterns)
- `./spec-reviewer-prompt.md` -- Dispatch spec compliance reviewer (interface conformance, commit discipline, over/under-building)
- `./code-quality-reviewer-prompt.md` -- Dispatch code quality reviewer (file growth, forbidden patterns, test quality)
- `./design-compliance-reviewer-prompt.md` -- Dispatch design compliance reviewer (token verification, typography, accessibility, Section 10)

---

## Integration

**Upstream:** This skill executes plans created by the writing-plans skill.

**Subagent skills:**
- **design-system-enforcer** — Design-aware subagents invoke this for full DESIGN.md grounding before writing code
- **test-reviewer** — Dispatch after writing test suite (>3 test cases in a single file) and before implementing. Fresh-context agent reviews tests for trivial passability, behavior vs implementation assertions, missing edge cases, and mock quality. Include test files + task description in the dispatch
- Subagents follow TDD by default (write test → verify fail → **test-reviewer gate** → implement → verify pass → **refactor** → verify stays green → commit)

**Design enforcement stack:**
- **Layer 2 hooks** (SessionStart, PreToolUse, SubagentStart) handle runtime token injection
- **This skill** handles structural execution, review gating, and verification
- If hooks inject different tokens than the micro-manifest's Design Context (because DESIGN.md changed since plan creation), **hooks take precedence** -- they read current state at write time

---

## Red Flags

**Never:**
- Start implementation on main/master branch without explicit user consent
- Skip reviews (spec compliance OR code quality OR design compliance when applicable)
- Proceed with unfixed issues from any review gate
- Dispatch multiple implementation subagents in parallel (conflicts)
- Make subagent read the plan file (provide full text in micro-manifest instead)
- Skip scene-setting context (subagent needs Architectural Context to understand where task fits)
- Ignore subagent questions (answer before letting them proceed)
- Accept "close enough" on spec compliance (reviewer found issues = not done)
- Skip review loops (reviewer found issues = implementer fixes = review again)
- Let implementer self-review replace actual review (both are needed)
- Start code quality review before spec compliance passes (wrong order)
- Start design compliance review before code quality passes (wrong order)
- Move to next task while any review gate has open issues
- Fix failed subagent tasks manually (context pollution) — dispatch a fix subagent with specific instructions instead
- Loop on fixes indefinitely (max 3 cycles per gate, then human escalation)
