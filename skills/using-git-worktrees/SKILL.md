---
name: using-git-worktrees
description: Use when creating multiple working copies of a repository for parallel agent work, reviewing a branch without disturbing current work, testing across branches, or dispatching independent tasks that need filesystem isolation
---

# Using Git Worktrees

## Overview

Git worktrees let you check out multiple branches simultaneously from a single repository. They share the object database and refs; each has its own HEAD, index, and working tree. This is the primary isolation mechanism for parallel AI agent work in 2026.

**Core principle:** Share the repo, isolate the checkout. Use Claude Code's native support first; fall back to raw git when scripting outside a Claude Code session.

**Announce at start:** "I'm using the using-git-worktrees skill to set up / clean up worktrees for this work."

## Mental Model

**Shared across all worktrees of a repo:**
- Object database (`.git/objects/` — all commits, trees, blobs)
- Refs (`refs/heads/` branches, `refs/tags/` tags) — unified namespace
- Main `config`

**Independent per worktree:**
- `HEAD` (which commit/branch this worktree is on)
- Index (staging area)
- Working tree files
- Per-worktree reflog

**`.git` in a linked worktree is a FILE, not a directory.** Inside, it's one line:
```
gitdir: /path/to/main/.git/worktrees/<id>
```
The main repo has the real `.git/` directory. Each linked worktree has a pointer. Some tools assume `.git/` is always a directory and break on worktrees — test compatibility before adopting org-wide.

**Same-branch invariant (memorize this):** Git refuses to check out the same branch in two worktrees simultaneously.
```
fatal: 'feature-x' is already checked out at '/path/to/other-worktree'
```
Use unique branches per worktree. Use `--detach` when you want a commit without a branch.

## When to Use a Worktree

**Use when:**
- Dispatching parallel agents to independent tasks (see dispatching-parallel-agents)
- Reviewing/testing a branch while your main work continues elsewhere
- Investigating a prior release without disturbing current branch state
- Running a long test suite in one worktree while you code in another

**Don't use when:**
- Single-branch hotfix — `git checkout -b fix && edit && commit` is simpler
- Two tasks on the same file — worktrees don't resolve the underlying conflict; sequence the work
- Short context switch (<10 minutes) — `git stash` is lighter than creating a worktree
- Tiny repo (<1K files, no monorepo setup cost) — cost > benefit

**Scale thresholds:**

| Simultaneous worktrees | Recommended approach |
|---|---|
| 1-4 | Raw `git worktree add` per task |
| 5-10 | Scripted helpers (shell aliases, `just` recipes) |
| >10 | Pool pattern (see Advanced Patterns) |

## Primary Path: Claude Code Native

When working inside Claude Code, prefer native worktree support over raw git. Native paths integrate with agent lifecycle and honour frontmatter declarations.

### `--worktree` flag

Start a Claude Code session inside an isolated worktree:
```bash
claude --worktree    # or: claude -w
```
The session runs in a fresh worktree sandbox. On exit, the worktree is cleaned up (or preserved with returned path + branch for review).

Raw-git equivalent (when scripting outside Claude Code):
```bash
git worktree add ../wt-<slug> -b <slug>
cd ../wt-<slug>
```

### `isolation: worktree` agent frontmatter

In subagent definitions, declare filesystem isolation:
```yaml
---
name: my-agent
description: ...
isolation: worktree
---
```
Dispatched subagents run in a fresh worktree. If they make no edits, the worktree is auto-removed. If they make edits, the path and branch return in the tool result — the user can review before merging.

Raw-git equivalent:
```bash
git worktree add ../wt-<agent-id> -b <agent-id>
# agent works in ../wt-<agent-id>
# on completion, dispatcher reviews and runs:
git worktree remove ../wt-<agent-id>   # or keep if agent produced changes
```

### EnterWorktree / ExitWorktree tools

Claude Code exposes tools for explicit lifecycle control. The **pattern** is stable even if tool names evolve:
- **Enter:** create a fresh worktree, optionally trigger setup hooks (install deps, run migrations)
- **Work:** the session/agent operates inside the worktree
- **Exit:** run validation, optionally create a PR, remove the worktree (or leave it for review)

Use these when you need explicit control over the enter/exit moments. Otherwise, the `--worktree` flag or `isolation: worktree` frontmatter handles lifecycle automatically.

## Raw Git Path: Commands & Lifecycle

Use these when scripting outside Claude Code (CI jobs, shell setup scripts, manual flows).

### Create

```bash
git worktree add ../wt-<slug> -b <branch-name>
```
- Place the new worktree **sibling** to the main repo (`../wt-<slug>`), **not nested** (`./branches/<slug>`). Nesting confuses `.gitignore`, editor file watchers, fd/ripgrep.
- `-b` creates a new branch. To check out an existing branch: `git worktree add ../wt-<slug> <existing-branch>`. To use a detached HEAD: `git worktree add --detach ../wt-<slug> <commit>`.

### List

```bash
git worktree list
```
Always verify before modifying. Output format:
```
/path/to/main        abc1234 [main]
/path/to/wt-feat     def5678 [feature-x]
```

### Remove (safe)

```bash
git worktree remove <path>
```
- Refuses on dirty working tree or unlocked-but-required worktree. This is the default cleanup command.
- Use `--force` ONLY after explicit user confirmation that any dirty state is intentional to discard.

### Prune (recovery only)

```bash
git worktree prune
```
- Removes stale administrative entries for worktrees whose directories were deleted manually.
- NOT a first-line cleanup tool. Use `git worktree remove` for routine cleanup. Prune is what you run after someone did `rm -rf ../wt-x` instead of using `remove`.

### Lock (protect)

```bash
git worktree lock <path> --reason "long-running release branch"
git worktree unlock <path>   # required before remove
```
- Prevents accidental `prune`. Use for long-running worktrees (release branches, pool slots).

### Pre-removal checklist

Before running `git worktree remove`:

1. **`git status` clean** inside the target worktree.
2. **Commits pushed** (if branch tracks a remote) — `git rev-list @{u}..HEAD` should be empty, or the work is being discarded intentionally.
3. **Branch state known** — merged, PR created, or explicitly discarded.

If any fails: resolve or confirm discard. Don't `--force` unless the dirty state is genuinely disposable.

## Top Pitfalls

### 1. Same-branch invariant (repeat)

```
fatal: 'feature-x' is already checked out at '/path/to/other'
```
Each worktree needs a unique branch. If you need "the same work" in two places, you don't — you need two distinct branches, OR one worktree plus a second editor window.

### 2. `node_modules` duplication kills disk + install time

Each worktree gets its own `node_modules`. On monorepos with many worktrees, this explodes.

**Fix (best):** use **pnpm** — its content-addressable global store hardlinks packages across worktrees. `pnpm install` is near-instant after the first.

**Fix (alternative):** Bun (fast install). Or a pre-warmed worktree pool (Advanced Patterns).

**Don't:** use npm-classic or yarn-classic on monorepos with 5+ worktrees. It's painful and you'll regret it.

### 3. Hooks don't share across worktrees

`.git/hooks/` is per-worktree. Team hooks installed there only fire in one worktree.

**Fix:** set `core.hooksPath` to a repo-tracked directory. Hooks committed to the repo work in every worktree.
```bash
git config core.hooksPath .githooks
```
Commit `.githooks/` to the repo. Husky-style tools configure this automatically.

### 4. Nested worktrees break tooling

Placing worktrees inside the main repo (`./branches/wt-x`) confuses `.gitignore`, editor file watchers, fd/ripgrep, language-server file crawlers.

**Fix:** always **sibling** to the main repo (`../wt-<slug>`).

### 5. Concurrent `git gc` corrupts shared state

Multiple worktrees calling `gc` simultaneously is a race. `gc --auto` can trigger automatically.

**Fix in each worktree:**
```bash
git config gc.auto 0
```
Centralize maintenance in the main repo. Run `git gc` during quiet hours, never in parallel.

### 6. Tool compatibility: some tools assume `.git/` is a directory

Breaks when `.git` is a file pointer in a worktree. Known affected: older git-lfs versions, spec-kit, some CI tooling.

**Fix:** test tooling in a worktree before adopting org-wide. Check that hooks run (`core.hooksPath`), submodules init (`git submodule update --init` per worktree), LFS fetches (`git lfs fetch && git lfs checkout`).

### 7. Windows: path length + rename atomicity

Windows 260-char path limit hits with deep worktree names + long package paths. Rename atomicity semantics differ from POSIX.

**Fix:** short worktree names. Enable long paths:
```bash
git config --global core.longpaths true
```
Test on Windows if the team is mixed-OS.

## Advanced Patterns (reference)

Concise pointers — full implementation lives in the linked tools.

### Bare-repo "pro" pattern

Central bare clone with sibling worktrees. Canonical 2026 layout for senior/monorepo workflows.
```bash
git clone --bare <url> <project>.git
cd <project>.git
git worktree add ../<project>/main main
# future:  git worktree add ../<project>/feature-x -b feature-x
```
Deep guide: https://fsck.sh/en/blog/git-worktree/. Note: a regular (non-bare) clone + worktrees gives ~95% of the benefit with less complexity — use bare only when you specifically want the repo-less-working-tree property.

### Pool pattern (scale to many agents)

Pre-created worktree "slots" claimed and released by agents. For >10 parallel agents or workloads dominated by setup time. Implementation coordinates slots via lockfiles, returns worktrees to pristine state on release:
```bash
git reset --hard
git clean -fdx
```
Tooling:
- Worktrunk — https://github.com/max-sixty/worktrunk
- workmux — https://github.com/raine/workmux

Not needed day-to-day. Adopt only when raw `git worktree add` is the bottleneck.

### Sparse-checkout combo

For monorepos where an agent/worktree only needs a subset of the tree:
```bash
git worktree add ../wt-api -b api-work
cd ../wt-api
git sparse-checkout init --cone
git sparse-checkout set packages/api packages/shared
```
Guide: https://github.blog/open-source/git/bring-your-monorepo-down-to-size-with-sparse-checkout/

## Quick Reference

| Task | Command |
|---|---|
| Create worktree on new branch | `git worktree add ../wt-<slug> -b <slug>` |
| Create worktree on existing branch | `git worktree add ../wt-<slug> <branch>` |
| Create detached (no branch) | `git worktree add --detach ../wt-<slug> <commit>` |
| List all worktrees | `git worktree list` |
| Safe remove | `git worktree remove <path>` |
| Force remove (confirm first) | `git worktree remove --force <path>` |
| Recover stale metadata | `git worktree prune` |
| Lock (protect from prune) | `git worktree lock <path>` |
| Unlock | `git worktree unlock <path>` |

| Rule | Why |
|---|---|
| Siblings, not nested | Nesting breaks .gitignore, editors, fd/ripgrep |
| Unique branch per worktree | Git refuses same-branch in 2 worktrees |
| Use pnpm (JS/TS) | Content-addressable store de-duplicates node_modules |
| `core.hooksPath` | Per-worktree `.git/hooks/` doesn't share |
| No concurrent `gc` | Corrupts shared object DB |

## Red Flags

**Never:**
- Manually `rm -rf` a worktree directory — leaves orphan metadata. Use `git worktree remove`, or run `prune` after if you already deleted the dir
- Run `git gc` in multiple worktrees concurrently
- Check out the same branch in two worktrees
- Nest worktrees inside the main repo
- Use npm-classic / yarn-classic on monorepos with 5+ worktrees
- Force-remove a dirty worktree without explicit confirmation that the dirty state is disposable

**Always:**
- Place worktrees sibling to main repo (`../wt-<slug>`)
- Use unique branches per worktree
- Run `git status` clean check before `git worktree remove`
- Configure `core.hooksPath` for team hooks
- Test tooling compatibility with worktrees before adopting broadly
- Prefer Claude Code native (`--worktree`, `isolation: worktree`) inside Claude Code sessions

## Rationalizations the agent will try

| Excuse | Reality |
|---|---|
| "I'll just nest the worktree under the main repo, it's cleaner" | Nested breaks .gitignore / editor / fd / ripgrep. Sibling is the convention for a reason. |
| "I can rm -rf the worktree directory, that's the same thing" | Leaves orphan metadata in `.git/worktrees/<id>/`. Use `git worktree remove` or run `prune` after. |
| "Using the same branch in two worktrees is fine if I'm careful" | Git refuses. Not a policy — an invariant. Use unique branches. |
| "npm is fine, I only have 3 worktrees" | 3 worktrees × 500MB node_modules = 1.5GB. pnpm is 500MB total. Switch now, not later. |
| "Hooks in `.git/hooks/` worked in my main checkout, that's enough" | Per-worktree. Other worktrees skip them silently. Use `core.hooksPath`. |
| "`gc --auto` in parallel is probably fine" | "Probably fine" = race condition waiting to corrupt your object DB. Disable `gc.auto` in worktrees. |
| "Claude Code's `--worktree` flag is just a wrapper, I'll use raw git" | Native integrates with agent lifecycle and frontmatter. Use native inside Claude Code; raw outside. |
| "Pool pattern looks cool, I'll set one up for my 3-agent workflow" | Overkill below 10 agents. Raw `git worktree add` per task is simpler. |

## Integration

**Called by:**
- **dispatching-parallel-agents** — setup for parallel agent work. That skill currently has a one-liner fallback; prefer this skill when available for full lifecycle + pitfalls + advanced patterns.

**Pairs with:**
- **finishing-a-development-branch** — Step 5 cleanup uses this skill's lifecycle commands. finishing owns the decision (should we remove?); this skill owns the mechanics (how to remove safely).

**Does NOT replace:**
- `git branch` for single-branch work
- `git stash` for short-lived context switches (<10 minutes)
- Full repository clones when you need a truly separate object database (rare — almost always worktrees suffice)
