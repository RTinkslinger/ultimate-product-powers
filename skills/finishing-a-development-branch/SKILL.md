---
name: finishing-a-development-branch
description: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup
---

# Finishing a Development Branch

## Overview

Guide completion of development work by presenting clear options and handling chosen workflow.

**Core principle:** Verify tests → Present options → Execute choice → Clean up.

**Announce at start:** "I'm using the finishing-a-development-branch skill to complete this work."

## The Process

### Step 1: Pre-Completion Verification

**Before presenting options, ALL of the following must pass:**

**1a. Tests**
```bash
# Run project's test suite
npm test / cargo test / pytest / go test ./...
```

**1b. Lint and type checks**
```bash
# Run lint + type check (project-specific)
npm run lint / ruff check . / cargo clippy
npx tsc --noEmit  # TypeScript type check
```

**1c. AI completeness scan**

AI agents consistently claim "done" while leaving artifacts behind. Before presenting options, scan for:
- [ ] Stale imports — modules imported but no longer used after changes
- [ ] Dead code — functions/variables that lost all callers during the work
- [ ] Leftover TODO/FIXME/HACK comments from the implementation
- [ ] Config pointing at old names — test configs, CI files, package.json scripts referencing renamed/deleted files
- [ ] Console.log / debug statements that shouldn't ship

```bash
# Quick scan
grep -rn "TODO\|FIXME\|HACK\|console\.log\|debugger" src/ --include="*.ts" --include="*.tsx" --include="*.js"
```

**1d. Design compliance (when DESIGN.md exists)**

If project root has DESIGN.md, verify the branch's frontend changes use design tokens correctly:
- Colors use CSS variables or Tailwind semantic classes from DESIGN.md Section 2 (no hardcoded hex)
- Typography matches Section 3 hierarchy
- Component patterns match Section 4

Skip this check if no DESIGN.md exists or no frontend files were changed.

**If ANY check fails:**
```
Pre-completion verification failed:

[Show failures by category]

Must fix before completing. Cannot proceed to merge/PR.
```

Stop. Don't proceed to Step 2.

**If ALL pass:** Continue to Step 2.

### Step 2: Determine Base Branch

```bash
# Try common base branches
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

Or ask: "This branch split from main - is that correct?"

### Step 3: Present Options

Present exactly these 4 options:

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

**Don't add explanation** - keep options concise.

### Step 4: Execute Choice

#### Option 1: Merge Locally

```bash
# Switch to base branch
git checkout <base-branch>

# Pull latest
git pull

# Merge feature branch
git merge <feature-branch>

# Verify tests on merged result
<test command>

# If tests pass
git branch -d <feature-branch>
```

Then: Cleanup worktree (Step 5)

#### Option 2: Push and Create PR

```bash
# Push branch
git push -u origin <feature-branch>

# Create PR
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<2-3 bullets of what changed>

## Test Plan
- [ ] <verification steps>
EOF
)"
```

Then: Cleanup worktree (Step 5)

#### Option 3: Keep As-Is

Report: "Keeping branch <name>. Worktree preserved at <path>."

**Don't cleanup worktree.**

#### Option 4: Discard

**Confirm first:**
```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

Wait for exact confirmation.

If confirmed:
```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

Then: Cleanup worktree (Step 5)

### Step 5: Cleanup Worktree

**For Options 1, 2, 4:**

Check if in worktree:
```bash
git worktree list | grep $(git branch --show-current)
```

If yes:
```bash
git worktree remove <worktree-path>
```

**For Option 3:** Keep worktree.

## Quick Reference

| Option | Merge | Push | Keep Worktree | Cleanup Branch |
|--------|-------|------|---------------|----------------|
| 1. Merge locally | ✓ | - | - | ✓ |
| 2. Create PR | - | ✓ | ✓ | - |
| 3. Keep as-is | - | - | ✓ | - |
| 4. Discard | - | - | - | ✓ (force) |

## Common Mistakes

**Skipping pre-completion verification**
- **Problem:** Merge code with failing tests, lint errors, or stale artifacts
- **Fix:** Run full pre-completion verification (tests + lint + AI completeness scan + design compliance) before offering options

**Premature "done" claim**
- **Problem:** AI agent fixes the obvious issues but leaves stale imports, dead code, leftover debug statements, config pointing at old names
- **Fix:** AI completeness scan catches these artifacts. Don't trust that the branch is clean — verify it

**Open-ended questions**
- **Problem:** "What should I do next?" → ambiguous
- **Fix:** Present exactly 4 structured options

**Automatic worktree cleanup**
- **Problem:** Remove worktree when might need it (Option 2, 3)
- **Fix:** Only cleanup for Options 1 and 4

**No confirmation for discard**
- **Problem:** Accidentally delete work
- **Fix:** Require typed "discard" confirmation

## Red Flags

**Never:**
- Proceed with failing tests, lint errors, or type errors
- Merge without running full pre-completion verification
- Skip the AI completeness scan ("it's probably clean" = it isn't)
- Delete work without confirmation
- Force-push without explicit request

**Always:**
- Run full pre-completion verification before offering options
- Present exactly 4 options
- Get typed confirmation for Option 4
- Clean up worktree for Options 1 & 4 only

## Integration

**Called by:**
- **executing-plans** - After all tasks/batches complete

**Pairs with:**
- **using-git-worktrees** - Cleans up worktree created by that skill
