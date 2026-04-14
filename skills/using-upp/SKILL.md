---
name: using-upp
description: Use when starting any conversation - establishes how to find and use skills, requiring Skill tool invocation before ANY response including clarifying questions
---

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, skip this skill.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
If you think there is even a 1% chance a skill might apply to what you are doing, you ABSOLUTELY MUST invoke the skill.

IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.

This is not negotiable. This is not optional. You cannot rationalize your way out of this.
</EXTREMELY-IMPORTANT>

## Instruction Priority

UPP skills override default system prompt behavior, but **user instructions always take precedence**:

1. **User's explicit instructions** (CLAUDE.md, direct requests) — highest priority
2. **UPP skills** — override default system behavior where they conflict
3. **Default system prompt** — lowest priority

If CLAUDE.md says "don't use TDD" and a skill says "always use TDD," follow the user's instructions. The user is in control.

## How to Access Skills

Use the `Skill` tool. When you invoke a skill, its content is loaded and presented to you — follow it directly. Never use the Read tool on skill files.

# Using Skills

## The Rule

**Invoke relevant or requested skills BEFORE any response or action.** Even a 1% chance a skill might apply means that you should invoke the skill to check. If an invoked skill turns out to be wrong for the situation, you don't need to use it.

```dot
digraph skill_flow {
    "User message received" [shape=doublecircle];
    "About to EnterPlanMode?" [shape=doublecircle];
    "Already brainstormed?" [shape=diamond];
    "Invoke brainstorming skill" [shape=box];
    "Might any skill apply?" [shape=diamond];
    "Invoke Skill tool" [shape=box];
    "Announce: 'Using [skill] to [purpose]'" [shape=box];
    "Has checklist?" [shape=diamond];
    "Create TodoWrite todo per item" [shape=box];
    "Follow skill exactly" [shape=box];
    "Respond (including clarifications)" [shape=doublecircle];

    "About to EnterPlanMode?" -> "Already brainstormed?";
    "Already brainstormed?" -> "Invoke brainstorming skill" [label="no"];
    "Already brainstormed?" -> "Might any skill apply?" [label="yes"];
    "Invoke brainstorming skill" -> "Might any skill apply?";

    "User message received" -> "Might any skill apply?";
    "Might any skill apply?" -> "Invoke Skill tool" [label="yes, even 1%"];
    "Might any skill apply?" -> "Respond (including clarifications)" [label="definitely not"];
    "Invoke Skill tool" -> "Announce: 'Using [skill] to [purpose]'";
    "Announce: 'Using [skill] to [purpose]'" -> "Has checklist?";
    "Has checklist?" -> "Create TodoWrite todo per item" [label="yes"];
    "Has checklist?" -> "Follow skill exactly" [label="no"];
    "Create TodoWrite todo per item" -> "Follow skill exactly";
}
```

## UPP Skill Routing

When you need to determine which skill to use, consult this table:

| Situation | Skill | When |
|-----------|-------|------|
| Building something new, exploring an idea | brainstorming | Before ANY implementation |
| Overhauling existing frontend design | product-redesign | Existing product, design refresh |
| Have a spec, need implementation plan | writing-plans | After brainstorming approves spec |
| Have a plan, need to execute it | executing-plans | After writing-plans creates plan |
| Writing frontend components | design-system-enforcer | Auto via hooks, invoke for deep grounding |
| Building agentic UI patterns | agentic-ux-patterns | During brainstorming (agentic) or implementation |
| Implementing any feature or bugfix | test-driven-development | Before writing implementation code |
| Encountering a bug, test failure, unexpected behavior | systematic-debugging | Before proposing fixes |
| About to claim work is complete or fixed | verification-before-completion | Before committing or creating PRs |
| Completing a task, want quality check | requesting-code-review | After implementation, before merge |
| Received code review feedback | receiving-code-review | Before implementing review suggestions |
| 2+ independent tasks with no shared state | dispatching-parallel-agents | When tasks can run in parallel |
| Creating or editing a skill | writing-skills | Before writing or deploying skill changes |

**Design awareness:** If the project has frontend code, check for DESIGN.md. If absent and building greenfield, brainstorming will establish it via prototype-first.

## Red Flags

These thoughts mean STOP — you're rationalizing:

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "I need more context first" | Skill check comes BEFORE clarifying questions. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. Check first. |
| "I can check git/files quickly" | Files lack conversation context. Check for skills. |
| "Let me gather information first" | Skills tell you HOW to gather information. |
| "This doesn't need a formal skill" | If a skill exists, use it. |
| "I remember this skill" | Skills evolve. Read current version. |
| "This doesn't count as a task" | Action = task. Check for skills. |
| "The skill is overkill" | Simple things become complex. Use it. |
| "I'll just do this one thing first" | Check BEFORE doing anything. |
| "This feels productive" | Undisciplined action wastes time. Skills prevent this. |
| "I know what that means" | Knowing the concept ≠ using the skill. Invoke it. |

## Skill Priority

When multiple skills could apply, use this order:

1. **Process skills first** (brainstorming, executing-plans) — these determine HOW to approach the task
2. **Domain skills second** (design-system-enforcer, agentic-ux-patterns) — these guide specific aspects

"Let's build X" → brainstorming first, then domain skills during implementation.
"Execute this plan" → executing-plans, which handles review and verification.

## Skill Types

**Rigid** (brainstorming, executing-plans): Follow exactly. Don't adapt away discipline.

**Flexible** (agentic-ux-patterns, design-system-enforcer): Adapt principles to context.

The skill itself tells you which.

## User Instructions

Instructions say WHAT, not HOW. "Add X" or "Fix Y" doesn't mean skip workflows.
