# L4 Integration Tests — Deferred

Integration tests (full chain execution on scaffold projects) are deferred to v2 of the test harness.

The audit pipeline's chain-interaction checks cover chain interactions until a regression proves L4 is needed.

Preserved design for v2:
- Chain 1: security-review -> security-reviewer agent (Flask scaffold)
- Chain 2: requesting -> code-reviewer -> receiving (Node.js scaffold)
- Chain 3: executing-plans full dispatch (Python scaffold)
- Each scaffold <20 files, plus one "unseen scaffold" per chain
