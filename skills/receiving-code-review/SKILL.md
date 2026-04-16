---
name: receiving-code-review
description: Use when receiving code review feedback, before implementing suggestions
---

# Receiving Code Review

## Core Principle

Code review requires technical evaluation, not emotional performance. Verify before implementing. Evidence before agreement. Technical correctness over social comfort.

**Announce:** "I'm using the receiving-code-review skill to process this feedback."

## Response Chain

```
WHEN receiving code review feedback:

1. READ: Complete all feedback without reacting.
   Trap: "I already know what they'll say." Counter: read it. You don't.

2. UNDERSTAND: Restate the requirement in own words (or ask).
   Trap: "This is obvious." Counter: misunderstandings hide in "obvious" items. Restate.
   IF any item is unclear: STOP. Ask for clarification on ALL unclear items before
   implementing anything. Partial understanding = wrong implementation.

3. VERIFY: Check against codebase reality.
   Trap: "The reviewer is clearly right, I don't need to check." Counter: verification
   is mandatory even when the reviewer seems correct. Read the actual code.

4. EVALUATE: Technically sound for THIS codebase?
   Trap: "It's a best practice, so it must apply." Counter: best practices have contexts.
   Check if this one applies here, to this stack, with these constraints.

5. RESPOND: Technical acknowledgment OR evidence-based pushback.
   Trap: "Great point!" Counter: FORBIDDEN. State the fix, or state why it's wrong.
   Pushback requires evidence: exit code, file:line, test output, or SARIF artifact.

6. IMPLEMENT: Highest-severity first, test each.
   Trap: "Let me do the easy ones first." Counter: severity order. Critical before cosmetic.
   Test each fix individually. Verify no regressions.
```

## Forbidden Responses

**NEVER:**
- "You're absolutely right!" / "Great point!" / "Excellent feedback!"
- "Thanks for catching that!" / any gratitude expression
- "Let me implement that now" (before verification)

**INSTEAD:**
- "Fixed. [Brief description of what changed]"
- "Good catch — [specific issue]. Fixed in [location]."
- Just fix it and show in the code. Actions speak.
- Push back with technical reasoning if wrong.

When feedback IS correct: state the fix or just do it. No ceremony.
When you pushed back and were wrong: "Verified — you're correct. [Reason my initial read was wrong]. Fixing."

## AI Failure Modes

| Pattern | What it looks like | Rationalization | Counter |
|---|---|---|---|
| **Performative agreement** | Immediate acceptance, praise phrases, no verification | "Being agreeable is being helpful" | Agreeable is not helpful. Accurate is helpful. Cite evidence or fix silently. |
| **False rebuttal** | Confident pushback without evidence; "I checked and it works" with no exit code | "I'm pretty sure this is fine" | Pushback requires falsifiable evidence. "Pretty sure" is not evidence. |
| **Scope drift** | Implementing more than asked (bonus refactoring) or less (skipping the hard part) | "While I'm here..." / "This part isn't really what they meant" | Implement exactly what was requested. Bonus work needs its own review cycle. |
| **Evidence-free pushback** | "I disagree because [reasoning]" without citing code, tests, or output | "My reasoning is sufficient" | Reasoning alone is insufficient. Cite the specific code, test, or output. |
| **Routing avoidance** | Handling design feedback inline instead of deferring to the appropriate skill | "I can handle this myself" | If feedback matches routing criteria below, route. Don't override the decision tree. |

## Structured Feedback Handling

When reviewer emits structured output (JSON with severity, category, line reference):

```
1. PARSE: Extract findings from structured output.
2. DEDUPLICATE: Fingerprint by file:line:rule_id. Remove exact and near-duplicates.
3. SORT: severity × confidence × blast_radius. Highest score first.
4. PROCESS: Apply Response Chain steps 3-6 to each finding, starting from highest severity.
```

When reviewer emits prose:

```
1. DECOMPOSE: Break comment into premises + conclusion.
   Example: "This API is vulnerable to injection" →
     Premise 1: user input reaches the query
     Premise 2: no sanitization exists
     Conclusion: injection is possible
2. EVALUATE each premise independently against codebase.
3. RESPOND to the weakest premise, not the conclusion.
4. If ALL premises hold → implement. If ANY premise false → pushback on that premise.
```

## Source-Specific Handling

### From the user
- Trusted — implement after understanding
- Still verify scope if ambiguous
- No performative agreement (same rule applies to all sources)
- Skip to action or technical acknowledgment

### From AI reviewer agents (code-reviewer, test-reviewer)
- Findings are hypotheses, not facts. Verify each against codebase.
- Weight structural observations higher (naming, architecture, patterns — the reviewer sees the code).
- Weight "this doesn't work" claims lower — the reviewer has limited execution context.
- If finding references a specific file:line, verify the file exists and line content matches.
- If finding suggests a fix, verify the fix compiles and passes before accepting.

### From external reviewers
- Skeptical evaluation — check if technically correct for THIS codebase.
- YAGNI check: if reviewer suggests "implementing properly," grep for actual usage first. If unused, flag it.
- Check if suggestion breaks existing functionality or conflicts with architectural decisions.
- If feedback conflicts with the user's prior decisions, stop and discuss with the user first.

## Conditional Routing

Routing is a CONSEQUENCE of the Evaluate step (Step 4), not a replacement. Evaluate FIRST, then route IF criteria met.

```
AFTER evaluating feedback (Step 4):

IF about design tokens, typography, component patterns, or visual styling
   AND DESIGN.md exists in project root:
   → Defer to design-system-enforcer for design-compliance evaluation.

IF flags a suspected bug AND meets ANY:
   severity ≥ High, blast radius wide, intermittent/non-reproducible,
   or reviewer says "root cause unclear":
   → Invoke systematic-debugging before patching. Root-cause first.

IF about test quality, coverage, or test design:
   → Cross-reference with test-driven-development skill.

ELSE:
   → Handle inline via Response Chain steps 5-6.
```

## Deadlock Resolution

When evidence-based pushback doesn't resolve after 2 rounds of evidence exchange:

1. Dispatch a **second-opinion agent** via Agent tool — fresh context, no prior conversation.
2. Provide both positions with cited evidence plus the code in question.
3. Do NOT include either party's conversation history or chain-of-thought.
4. Arbiter delivers verdict with reasoning. If uncertain, escalate to user with all positions.

## Integration Points

**Evidence vocabulary:** falsifiable artifact = exit code, test runner output, git SHA, diff, coverage delta, SARIF. Self-report ("tests pass") is the weakest tier.

**verification-before-completion** — When pushing back on reviewer claims, cite evidence per verification's hierarchy: exit code > structured artifact > static inference > self-report. "I checked and it works" is the weakest form. "Exit 0, ran `pytest tests/auth.py -v`, 12/12 passed" is Tier 1 evidence.

**systematic-debugging** — When reviewer flags a potential bug, do not patch the symptom. Invoke systematic-debugging's root-cause pipeline: reproduce → hypothesize → isolate → fix → verify.

**executing-plans** — When working under a plan, review feedback handling slots into the three-gate pipeline's quality gate. Process all review findings before marking the plan task complete.

## Red Flags

You are about to violate this skill if you catch yourself doing any of these. STOP and restart from Step 1:

- About to write "Great point!", "You're absolutely right!", "Thanks for catching that!"
- About to implement without verifying against codebase (Step 3 skipped)
- About to agree without restating the requirement in own words (Step 2 skipped)
- Pushing back without citing specific evidence (exit code, file:line, test output)
- About to implement all comments in batch without testing each individually
- Handling design feedback inline when DESIGN.md exists and routing criteria are met
- About to patch a symptom when reviewer flagged a potential root-cause bug
- Implementing more than reviewer asked (scope drift, bonus refactoring)
- "The reviewer is senior so they must be right" — authority is not evidence
- Accepting a suggestion that conflicts with the user's prior architectural decisions without checking
- About to say "I can't verify this" without offering to investigate
- Ignoring structured-feedback severity ordering (processing cosmetic before critical)

## When This Skill Fires

This skill fires when:
- Review feedback appears in conversation from ANY source (user, AI agent, external)
- The requesting-code-review skill dispatches a reviewer agent and findings return (auto-chain)
- Another skill (executing-plans, finishing-a-development-branch) routes review findings here

Trigger phrases: "here's my review", "review feedback", "issues found", "comments on your code", or any structured/prose review output in the conversation.

## The Bottom Line

Verify. Evaluate. Then implement.

No performative agreement. No evidence-free pushback. No routing avoidance.
Technical rigor, always.
