---
name: finishing-a-development-branch
description: Use when implementation is complete and you need to decide how to integrate the work — before claiming done, before merging, before creating a PR, before removing a worktree
---

# Finishing a Development Branch

## Overview

Guide completion of development work with pre-merge verification, then present options and handle the chosen workflow.

**Core principle:** Verify → advise → decide → execute → clean up.

**Announce at start:** "I'm using the finishing-a-development-branch skill to complete this work."

## The Process

### Step 1: Pre-Completion Verification

**Before presenting options, ALL of the following must pass. No exceptions.**

#### 1a. Tests — in a fresh terminal

```bash
# Run the project's test suite IN A FRESH TERMINAL
# (not the same shell session where changes were authored)
npm test / cargo test / pytest / go test ./...
```

**Why fresh terminal:** AI agents hallucinate test results in-session. Cached shell state can make a failing suite appear to pass. A clean shell with no residual state is the minimum ground-truth check. **Paste the exit code before continuing — do not infer from log lines.**

#### 1b. Lint and type checks

```bash
npm run lint / ruff check . / cargo clippy
npx tsc --noEmit  # TypeScript type check
```

#### 1c. AI completeness scan

AI agents claim "done" while leaving artifacts behind. Before presenting options, scan for:

- **Stale imports** — run the project's linter. `eslint` / `ruff check --select F401` / `tsc`. Grep WILL NOT catch unused imports — the AST check does.
- **Dead code** — `npx knip` (JS/TS) or `vulture` (Python). If a function has zero callers outside its definition, it's dead.
- **Leftover TODO/FIXME/HACK added during this branch** (not pre-existing):
  ```bash
  git diff <base-branch> -- '*.ts' '*.tsx' '*.js' '*.py' | grep -E '^\+.*\b(TODO|FIXME|HACK)\b'
  ```
- **Config pointing at old names** — test configs, CI files, `package.json` scripts referencing renamed/deleted files.
- **Debug statements that shouldn't ship** (text search is valid here):
  ```bash
  git diff <base-branch> --name-only | xargs grep -n "console\.log\|debugger\|print(" 2>/dev/null
  ```

#### 1d. Design compliance (when DESIGN.md exists)

If project root has DESIGN.md AND this branch changed frontend files:

Invoke the **design-system-enforcer** skill for a compliance audit, or at minimum:
```bash
# Scan changed frontend files for hardcoded hex colors (should use tokens)
git diff <base-branch> --name-only -- '*.tsx' '*.jsx' '*.css' | xargs grep -n '#[0-9a-fA-F]\{3,8\}' 2>/dev/null
```

Hardcoded hex → should use CSS variables or Tailwind semantic classes from DESIGN.md Section 2. Check typography matches Section 3. Check component patterns match Section 4.

Skip if no DESIGN.md exists or no frontend files changed.

#### 1e. Diff self-consistency — check for AI workarounds

AI agents sometimes modify infra/config files as workarounds instead of fixing the root cause (bump a package version to silence an error, add a TS ignore, disable a lint rule).

```bash
# Flag suspicious changes in infra/config files (top-level OR nested in monorepo)
git diff <base-branch> --name-only | grep -E '(^|/)(package\.json|pnpm-lock\.yaml|yarn\.lock|package-lock\.json|tsconfig\.json|jsconfig\.json|pyproject\.toml|requirements\.txt|Dockerfile|docker-compose\.yml)$|\.github/workflows/|\.circleci/|\.gitlab-ci\.yml$|azure-pipelines\.yml$'
```

If matches: **stop and ask** — "These infra/config files changed. Confirm each was intentional. If any was an AI workaround to silence an error, revert it and fix the underlying issue before proceeding."

#### If any check fails

```
Pre-completion verification failed:

[Show failures by category]

Must fix before completing. Cannot proceed to options.
```

Stop. Do not proceed to Step 2.

### Step 2: Determine Base Branch

```bash
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

Or ask: "This branch split from main — is that correct?"

### Step 2.5: PR Size Advisory

**Advisory, not a blocker.** Fires only when BOTH conditions are true:

```bash
loc=$(git diff --stat <base-branch> | tail -1 | awk '{print $4+$6}')
commits=$(git log <base-branch>..HEAD --oneline | wc -l)

if [[ $loc -gt 400 && $commits -gt 3 ]]; then
  echo ""
  echo "Branch is $loc LOC across $commits commits."
  echo "Research shows defect escape rate climbs from 4% (<200 LOC) to 28% (>800 LOC)."
  echo "Consider decomposing before merge — see dispatching-parallel-agents for sequential-merge pattern."
  echo ""
fi
```

This is a suggestion. User can proceed either way. Trivial one-commit branches that touched a large generated file skip this advisory (commits ≤ 3 threshold).

### Step 3: Present Options

**Detect audience first.** Before printing options:

```bash
has_remote=$(git remote -v | grep -c .)
has_ci=$(ls -d .github/workflows .circleci azure-pipelines.yml .gitlab-ci.yml 2>/dev/null | wc -l)
```

If both are non-zero, prepend this note to the options block:

```
Note: remote + CI detected. Option 2 (PR) runs CI verification that Option 1 skips.
Pick Option 1 only for solo/hobby contexts.
```

Then present exactly these 4 options:

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

**Don't add other explanation** — keep options concise beyond the audience note.

### Step 4: Execute Choice

#### Option 1: Merge Locally

**Pick a merge strategy first:**

```
Merge strategy:
  a. Squash — single clean commit, linear history (default if branch has >5 commits)
  b. Merge-commit — preserves branch history (default if ≤5 commits; use for audit-required features)

(If your team uses rebase-merge: `git rebase <base> && git merge --ff-only` instead.)

Which?
```

Default-suggest based on commit count; let user override.

**Execute:**

```bash
# Option 1a — Squash
git checkout <base-branch>
git pull
git merge --squash <feature-branch>
git commit   # opens editor — write a clean commit message

# Option 1b — Merge-commit (preserves branch topology)
git checkout <base-branch>
git pull
git merge --no-ff <feature-branch>

# Post-merge: re-run tests on merged result (in a fresh terminal)
<test command>

# If tests pass:
git branch -d <feature-branch>
```

Then: Cleanup worktree (Step 5).

#### Option 2: Push and Create PR

```bash
git push -u origin <feature-branch>

gh pr create --title "<concise title under 70 chars>" --body "$(cat <<'EOF'
## Summary
- <what changed, 2-3 bullets>
- <why it changed>

## Linked Issue
<#123 — or "n/a">

## Test Plan
- [ ] <verification steps>
- [ ] Fresh-terminal test run passed (Step 1a)

## Rollback
<revert command, feature flag path, or "revert the merge commit">

<!-- AI provenance (optional): model / scope of AI-generated code -->
EOF
)"
```

Fill or delete the AI provenance comment line. Required: Summary, Test Plan, Rollback. Issue and provenance optional.

Then: Cleanup worktree (Step 5).

#### Option 3: Keep As-Is

```
Keeping branch <name>. Worktree preserved at <path>.
```

**Do not cleanup worktree.**

#### Option 4: Discard

**Confirm first:**

```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

Wait for exact confirmation — no other word.

If confirmed:
```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

Then: Cleanup worktree (Step 5).

### Step 5: Cleanup Worktree

**For Options 1, 2, 4 only.** Option 3 keeps the worktree.

Check if current work is in a worktree:

```bash
current_branch=$(git branch --show-current)
current_worktree=$(git worktree list | grep "\[$current_branch\]$" | awk '{print $1}')
```

If in a worktree, run the pre-removal checklist:

```bash
cd "$current_worktree"

# 1. Working tree clean
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "Uncommitted changes in worktree. Commit, stash, or discard before removing."
  exit 1
fi

# 2. Local commits pushed (if remote tracking)
if [[ -n "$(git rev-list @{u}..HEAD 2>/dev/null)" ]]; then
  echo "Local commits not pushed to upstream. Push first OR confirm discard."
  # ask user to confirm
fi

# 3. Remove (safe — refuses on dirty state)
git worktree remove "$current_worktree"
```

If `git worktree remove` refuses: surface the error, don't force without explicit user confirmation.

**For Option 4 (discard):** the branch is already deleted — worktree removal is mechanical, but the pre-flight still applies (don't force-remove with hidden state).

For deeper worktree lifecycle guidance, invoke the **using-git-worktrees** skill if available. Fallback: the commands above plus `git worktree prune` for metadata cleanup after manual directory deletion.

## Quick Reference

| Option | Merge | Push | Keep Worktree | Cleanup Branch |
|--------|-------|------|---------------|----------------|
| 1. Merge locally | ✓ | - | - | ✓ |
| 2. Create PR | - | ✓ | ✓ | - |
| 3. Keep as-is | - | - | ✓ | - |
| 4. Discard | - | - | - | ✓ (force) |

| Verification step | Required | Tool |
|---|---|---|
| 1a Tests (fresh terminal) | Yes | project test suite |
| 1b Lint + type check | Yes | eslint/ruff/clippy + tsc |
| 1c AI completeness scan | Yes | linter + knip/vulture + git-diff grep |
| 1d Design compliance | If DESIGN.md + frontend changes | design-system-enforcer |
| 1e Diff self-consistency | Yes | git diff + file-name grep |

## Common Mistakes

**Skipping pre-completion verification**
- Problem: Merge code with failing tests, stale artifacts, or AI workarounds.
- Fix: Run Steps 1a–1e in order. Every step. No skipping because "it's probably clean."

**Premature "done" claim (in-session tests)**
- Problem: AI runs tests in the session where changes were made, gets a cached pass, claims done. Production breaks.
- Fix: Step 1a mandates fresh terminal. Paste the exit code — do not infer from chat output.

**AI modified infra files as a workaround**
- Problem: Agent bumps a package version to silence a real bug, adds a TS ignore, disables a lint rule.
- Fix: Step 1e flags infra/config changes. Investigate each one before proceeding.

**Grepping for unused imports**
- Problem: Grep can't detect unused imports — imports live in syntax, not text patterns.
- Fix: Use the linter (eslint / ruff / tsc). Grep is only valid for debug statements (text search works for `console.log`).

**Merging locally when CI exists**
- Problem: Option 1 skips the full CI gate (integration tests, security scans, dependency checks) that the repo relies on.
- Fix: Audience detection in Step 3 advises Option 2 when remote + CI. Option 1 is for solo/no-CI contexts.

**Dismissing the size advisory**
- Problem: 650-LOC branch merged as one PR; defect escape rate ~22% (Propel Code data).
- Fix: Step 2.5 advisory. Decomposition feels like overhead but cuts defect rate 4x. Use dispatching-parallel-agents sequential-merge pattern.

**Open-ended questions**
- Problem: "What should I do next?" → ambiguous. User gives a vague direction.
- Fix: Present exactly 4 structured options. Don't add extra options or commentary.

**Automatic worktree cleanup**
- Problem: Remove worktree when it's still needed (Option 2 PR awaiting review, Option 3 keep).
- Fix: Only cleanup for Options 1 and 4. Option 2 keeps worktree until PR merges elsewhere. Option 3 keeps by definition.

**Force-removing a dirty worktree**
- Problem: `git worktree remove --force` discards uncommitted changes silently.
- Fix: Step 5 pre-flight checklist catches this. Don't pass `--force` without explicit confirmation.

**No confirmation for discard**
- Problem: Accidentally delete work.
- Fix: Require typed "discard" confirmation — no other word accepted.

## Red Flags

**Never:**
- Proceed with failing tests, lint errors, or type errors
- Accept in-session test results as verification — Step 1a mandates fresh terminal
- Merge after AI modified infra files without confirming each change was intentional
- Skip the AI completeness scan ("it's probably clean" = it isn't)
- Pick Option 1 on a team project with CI (pick Option 2)
- Dismiss the size advisory because "my 650 LOC is cohesive"
- Force-remove a dirty worktree
- Delete work (Option 4) without typed confirmation
- Force-push without explicit request

**Always:**
- Run full pre-completion verification (1a–1e) before offering options
- Re-run tests in a fresh terminal — paste the exit code
- Check diff for infra-file changes (Step 1e)
- Detect audience before presenting options (remote + CI advisory)
- Present exactly 4 options — no more, no fewer
- Ask merge strategy on Option 1 (squash vs merge-commit)
- Use the PR body template on Option 2 (summary + issue + test plan + rollback)
- Pre-flight the worktree before removing (Step 5)
- Clean up worktree only for Options 1 & 4

## Rationalizations the agent will try

| Excuse | Reality |
|---|---|
| "Tests passed in my session, re-running is redundant" | In-session runs may hit cached state. Fresh terminal is the minimum ground-truth check. 30 seconds. Run it. |
| "Only lock files changed — those are always noise" | Lock file changes can hide silent dependency upgrades that break runtime behavior. Confirm intentional. |
| "Step 1e is paranoid — my infra changes are fine" | AI agents modify infra to silence errors. Take the 10 seconds to confirm. If you're right, fine. If you're wrong, you saved prod. |
| "My branch is 600 LOC but it's all one feature" | Cohesive ≠ reviewable. Reviewers skim past 400 LOC. Defect rate climbs. Decompose or accept the risk. |
| "I'll merge locally — CI takes too long" | CI exists to catch what local verification doesn't. Option 2 runs it. Option 1 skips it. The CI time is the point. |
| "Squash vs merge-commit doesn't matter for small PRs" | Matters for history bisection later. Pick squash for clean linear history, merge-commit for audit. Asking takes 5 seconds. |
| "My worktree has minor uncommitted changes, just force-remove" | Force-remove discards silently. Pre-flight catches this. Commit, stash, or explicitly discard. |
| "I can skip the PR body template on a tiny PR" | Required sections (test plan, rollback) are what the reviewer needs to merge safely. Tiny PR → tiny test plan, but still present. |

## Integration

**Called by:**
- **executing-plans** — after all tasks/batches complete

**Pairs with:**
- **verification-before-completion** — task-level verification during implementation. This skill handles branch-level verification at finish time. Both may check "tests pass" at different moments; that is intentional — they are separate verification events.
- **design-system-enforcer** — invoked from Step 1d for DESIGN.md compliance.
- **dispatching-parallel-agents** — referenced in Step 2.5 size advisory for sequential-merge decomposition pattern.
- **using-git-worktrees** — owns worktree lifecycle mechanics; Step 5 uses its cleanup commands. Fallback shown inline if that skill is not available.
