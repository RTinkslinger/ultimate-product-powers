# Code Quality Reviewer Prompt Template

Use this template when dispatching a code quality reviewer subagent.

**Purpose:** Verify implementation is well-built (clean, tested, maintainable)

**Only dispatch after spec compliance review passes.**

```
Task tool (general-purpose):
  description: "Review code quality for Task N"
  prompt: |
    You are reviewing the quality of an implementation that has already
    passed spec compliance review. The code does what was asked —
    your job is to verify it's well-built.

    WHAT_WAS_IMPLEMENTED: [from implementer's report]
    PLAN_OR_REQUIREMENTS: Task N from [plan-file]
    BASE_SHA: [commit before task]
    HEAD_SHA: [current commit]

    ## Your Job

    **Single responsibility:**
    - Does each file have one clear responsibility?
    - Are units decomposed so they can be understood and tested independently?
    - Is the implementation following the file structure from the plan?
    - Did this implementation create new files that are already large?

    **Code quality:**
    - Is the code clean, readable, and maintainable?
    - Are names clear and accurate?
    - Are there unnecessary abstractions or over-engineering?

    **Testing quality:**
    - Do tests actually verify behavior, not just mock behavior?
    - Is test coverage meaningful (not just high numbers)?
    - Are edge cases covered?

    **Forbidden patterns:**
    - Are there hardcoded values that should use design tokens or constants?
    - Any security concerns (command injection, XSS, SQL injection)?

    **File growth:**
    - Did this change significantly grow any existing files?
      (Don't flag pre-existing file sizes — focus on what this change contributed.)
    - Are new files appropriately sized?

    Report:
    - **Strengths:** What's well-done
    - **Issues:** (Critical / Important / Minor)
    - **Assessment:** Approved or Changes Required
```
