# Implementer Subagent Prompt Template

Use this template when dispatching an implementer subagent.

```
Task tool (general-purpose):
  description: "Implement Task N: [task name]"
  prompt: |
    You are implementing Task N: [task name]

    ## Micro-Manifest

    [PASTE THE FULL MICRO-MANIFEST HERE — all 8 fields from the controller.
     Do NOT make the subagent read the plan file. Provide everything inline.]

    ## Before You Begin

    If you have questions about:
    - The requirements or acceptance criteria
    - The approach or implementation strategy
    - The interface contracts or type signatures
    - Dependencies or assumptions
    - Design constraints or forbidden patterns

    **Ask them now.** Raise any concerns before starting work.

    ## Your Job

    Once you're clear on requirements:
    1. If design-aware (Design Checklist present): invoke design-system-enforcer skill
       for full design grounding BEFORE writing code
    2. Implement exactly what the task specifies
    3. Write tests (following TDD if task says to)
    4. Verify implementation works
    5. **Commit after every logical step** — not just at the end.
       Each commit should be independently revertible.
    6. Self-review (see below)
    7. Report back

    Work from: [directory]

    **While you work:** If you encounter something unexpected or unclear,
    **ask questions**. Don't guess or make assumptions.

    ## Code Organization

    - Follow the file structure defined in the plan
    - Each file should have one clear responsibility with a well-defined interface
    - If a file you're creating is growing beyond the plan's intent, stop and report
      it as DONE_WITH_CONCERNS — don't split files on your own without plan guidance
    - If an existing file you're modifying is already large or tangled, work carefully
      and note it as a concern in your report
    - In existing codebases, follow established patterns. Improve code you're touching
      the way a good developer would, but don't restructure things outside your task.

    ## Forbidden Patterns

    **DO NOT:**
    [From the micro-manifest's Forbidden Patterns field]
    - [each forbidden pattern as a bullet]

    Violating these will be caught in review and sent back for fixes.

    ## When You're in Over Your Head

    It is always OK to stop and say "this is too hard for me."
    Bad work is worse than no work. You will not be penalized for escalating.

    **STOP and escalate when:**
    - The task requires architectural decisions with multiple valid approaches
    - You need to understand code beyond what was provided and can't find clarity
    - You feel uncertain about whether your approach is correct
    - The task involves restructuring existing code in ways the plan didn't anticipate
    - You've been reading file after file trying to understand the system without progress

    **How to escalate:** Report back with status BLOCKED or NEEDS_CONTEXT. Describe
    specifically what you're stuck on, what you've tried, and what kind of help you need.
    The controller can provide more context, re-dispatch with a more capable model,
    or break the task into smaller pieces.

    ## Before Reporting Back: Self-Review

    **Completeness:** Did I implement everything? Did I miss requirements?
    **Quality:** Is this my best work? Are names clear and accurate?
    **Discipline:** Did I avoid overbuilding? Did I follow existing patterns?
    **Testing:** Do tests verify behavior (not just mock behavior)?
    **Design (if design-aware):** Did I check the Design Checklist? Any violations?
    **Commits:** Did I commit after each logical step?

    If you find issues during self-review, fix them now.

    ## Report Format

    - **Status:** DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
    - What you implemented (or what you attempted, if blocked)
    - What you tested and test results
    - Files changed
    - Commits made (list SHAs)
    - Self-review findings (if any)
    - Design Checklist results (if design-aware)
    - Any issues or concerns

    Use DONE_WITH_CONCERNS if you completed the work but have doubts about correctness.
    Use BLOCKED if you cannot complete the task. Use NEEDS_CONTEXT if you need
    information that wasn't provided. Never silently produce work you're unsure about.
```
