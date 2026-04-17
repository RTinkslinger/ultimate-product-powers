# Changelog

## [2.0.0] — 2026-04-17
Added: security-review skill, security-reviewer agent
- security-review: 3-step security gate (threat-model, scan, cite evidence), per-language SAST command table (5 ecosystems), Iron Law severity enforcement (critical/high = hard block), 6 AI-specific threat categories (prompt injection, slopsquatting, insecure output handling, config-as-attack-surface, tool poisoning, agent trust boundaries), 10x hardened slopsquatting verification protocol, secrets detection with rotation guidance, always-dispatch security-reviewer agent
- security-reviewer: adversarial reviewer in independent context, 6 AI-threat deep dives with grep detection patterns, independent SAST scan protocol, 5-dimension adversarial checklist, structured output format
- Plugin: 17 skills, 3 agents, 3 hooks

## [1.9.0] — 2026-04-17
Edited: receiving-code-review, requesting-code-review (UPP-native rebuild)
- receiving: 6-step response chain with inline rationalization traps, 5 AI failure modes, structured/prose dual-path feedback handling, 3-source handling (user/AI agent/external), conditional routing to 3 UPP skills, deadlock resolution via second-opinion agent, 12 red flags
- requesting: 4 mandatory trigger categories (all skip=No), canonical evidence bundle with redaction rule, agent dispatch protocol with fresh-context enforcement, 3 risk tiers, auto-chain to receiving, 8 red flags
- Voice: "your human partner" framing replaced with role-neutral language throughout
- Removed: Circle K easter egg, GitHub thread reply section, inline bash for SHA retrieval

## [1.8.1] — 2026-04-17
Edited: verification-before-completion (one-line cleanup)

## [1.8.0] — 2026-04-17
Edited: verification-before-completion (full pipeline rebuild, supersedes v1.7.0)

## [1.7.0] — 2026-04-16
Edited: verification-before-completion (superseded by v1.8.0)

## [1.6.0] — 2026-04-16
Added: using-git-worktrees
Edited: finishing-a-development-branch, dispatching-parallel-agents

## [1.5.0] — 2026-04-16
Edited: dispatching-parallel-agents

## [1.4.1] — 2026-04-16
Fixed: finishing-a-development-branch, dispatching-parallel-agents

## [1.4.0] — 2026-04-16
Added: finishing-a-development-branch
Edited: dispatching-parallel-agents

## [1.3.0] — 2026-04-16
Edited: systematic-debugging

## [1.2.0] — 2026-04-16
Edited: test-driven-development, executing-plans

## [1.1.0] — 2026-04-16
Edited: using-upp

## [1.0.0] — 2026-04-15
Initial release. Skills:

- brainstorming
- writing-plans
- executing-plans
- design-system-enforcer
- product-redesign
- agentic-ux-patterns
- test-driven-development
- systematic-debugging
- verification-before-completion
- requesting-code-review
- receiving-code-review
- writing-skills
- dispatching-parallel-agents
- using-upp
