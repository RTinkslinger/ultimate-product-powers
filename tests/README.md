# UPP Test Suite

Automated regression testing for the UPP plugin (17 skills, 3 agents, 3 hooks).

## Quick Start

```bash
cd tests
./run.sh -m quick           # L1 + hooks (<1 min, gating)
./run.sh                    # Everything: L1 + L2 + L3 + hooks (~60 min)
./run.sh -k security_review # Single skill
```

## Layers

| Layer | What | Runtime | Marker | Gates? |
|---|---|---|---|---|
| L1 | Content snapshots (grep patterns in SKILL.md files) | <1 sec | `quick` | **Yes** — pre-push |
| L2 | Trigger tests (claude -p headless, 68 prompts) | ~45 min | `full` | No — xfail, informational |
| L3 | Behavior RED-GREEN (6 core skills) | ~30 min | `full` | No — xfail where noted |
| Hooks | Bash hook smoke tests | <5 sec | `quick` | **Yes** — pre-push |

### Why L2 is informational (not gating)

L2 trigger tests run `claude -p` in headless mode and check whether the expected
skill is invoked via the Skill tool. This is **inherently probabilistic**:

- **Positive tests** fail ~20% of the time because the model answers directly
  without invoking any skill, despite having the routing table from SessionStart.
- **Negative tests** fail ~30% of the time because UPP's using-upp skill instructs
  "if even 1% chance a skill applies, invoke it" — causing broad over-invocation.

All 68 L2 tests use `xfail(strict=False)`. Passes are logged as xpass (welcome).
Failures are expected. Track routing quality trends in `test-results/` over releases.

## Requirements

- Python 3.10+
- Claude Code CLI (`claude --version`)
- UPP plugin installed (this repo)

## Adding Tests for a New Skill

1. Write manifest: `content_snapshots/manifests/<skill_name>.txt`
   - Include vocabulary anchors (key terms) and behavioral mandates (imperative sentences)
2. Write 4 prompts: `trigger/prompts/<skill>_{naive,explicit,kwabsent,negative}.txt`
3. Add 4 entries to `trigger/expected.json`
4. If core gate/enforcement skill: add task + markers to `behavior/`
5. Run: `./run.sh -k <skill_name>`

## Modifying an Existing Skill

1. Update manifest if required patterns changed
2. Run: `./run.sh -k <skill_name>`
3. If description changed: re-run L2 trigger tests

## Adding a New Agent

1. Write manifest: `content_snapshots/manifests/<agent_name>.txt`
2. Run: `./run.sh content_snapshots/ -k <agent_name>`

## Debugging Failures

### CONTENT REGRESSION
A required pattern is missing from a SKILL.md. Either:
- The pattern was intentionally removed → update the manifest
- The pattern was accidentally removed → restore it

### TRIGGER REGRESSION
The expected skill didn't fire. Check:
1. Did the skill's description change? Compare with git diff.
2. What skill DID fire? Check test output for "but got: [...]"
3. Is the prompt ambiguous? Multiple skills may validly match.

### NEGATIVE TRIGGER FAILURE
A skill fired when it shouldn't have. The description may be too broad.
Check which keywords in the description match the negative prompt.

### RED-GREEN INDISTINGUISHABLE
All GREEN markers also appeared in RED. The markers are in Claude's
training data, not skill-specific. Replace with more procedural markers.

## Test Results

Results are auto-saved to `test-results/<tag>.json` after each run.
Compare across releases to track regression trends.
