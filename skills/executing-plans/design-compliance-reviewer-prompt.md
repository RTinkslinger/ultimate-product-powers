# Design Compliance Reviewer Prompt Template

Use this template when dispatching a design compliance reviewer subagent.

**Purpose:** Verify implementation matches design system constraints from DESIGN.md.

**Only dispatch for design-aware tasks** (tasks with a `**Design Reference:**` block).
**Only dispatch after BOTH spec compliance AND code quality reviews pass.**

```
Task tool (general-purpose):
  description: "Review design compliance for Task N"
  prompt: |
    You are reviewing whether a frontend implementation matches
    the project's design system constraints. The code has already
    passed spec compliance and code quality reviews. Your job is
    strictly about design fidelity.

    ## Design Reference (from the plan task)

    [PASTE the task's Design Reference block — which DESIGN.md sections apply]

    ## Design Checklist (from the plan task)

    [PASTE the task's Design Checklist block]

    ## DESIGN.md Sections

    [PASTE the specific DESIGN.md sections referenced in the Design Reference.
     Do NOT paste the entire DESIGN.md — only the sections this task references.]

    ## What Was Implemented

    [From implementer's report — files changed, design checklist self-assessment]

    ## CRITICAL: Do Not Trust the Self-Assessment

    The implementer checked their own Design Checklist. Verify independently.

    ## Your Job

    Read the actual implementation files and verify:

    **Semantic tokens (Section 2):**
    - Run: `grep -rn '#[0-9a-fA-F]\{3,8\}' [component files]`
    - Any hardcoded hex values? Flag each with file:line
    - All colors should use CSS variables or Tailwind semantic classes

    **Typography (Section 3):**
    - Font families match DESIGN.md hierarchy?
    - Font sizes use the scale from Section 3 (not arbitrary values)?
    - Font weights are correct?

    **Component patterns (Section 4):**
    - Border-radius matches Section 4 (e.g., `rounded-lg` not `rounded-[7px]`)?
    - Padding/spacing follows Section 4 patterns?
    - Shadow usage matches Section 4?

    **Accessibility:**
    - Semantic HTML used (button not div with onClick)?
    - ARIA attributes present where needed?
    - Color contrast >= 4.5:1 for normal text, >= 3:1 for large text?
    - Focus states visible on interactive elements?

    **Section 10 compliance (if agentic product):**
    - Does the component match a registered JSON type from Section 10?
    - Are the expected props and states handled?
    - Does the fallback renderer handle unknown types?

    **Design-system-enforcer skill:**
    - Did the implementer invoke the design-system-enforcer skill?
    - Check their report — if not mentioned, flag it

    Report:
    - ✅ Design compliant
    - ❌ Issues found: [list with file:line references and which
      DESIGN.md section is violated. Be specific:
      "src/components/Card.tsx:15 — hardcoded #1a1a2e, should use
      var(--background) per DESIGN.md Section 2"]
```
