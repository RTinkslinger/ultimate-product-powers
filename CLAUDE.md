# UPP Plugin — Distribution Repo

This is the **distribution repo** for Ultimate Product Powers. What's here is what ships to users.

## Development Workflow

Development happens in the dev workspace at `~/Claude Projects/Skills Factory/Ultra Product Powers/`. This repo receives finished skills — it is NOT where research, specs, or plans live.

**Flow:**
1. Research + brainstorm + spec + plan → dev workspace
2. Build skill → dev workspace `skills/<name>/SKILL.md`
3. Copy finished skill → this repo `skills/<name>/`
4. Commit + push → GitHub (`RTinkslinger/ultimate-product-powers`)
5. Users install → `/plugin marketplace add RTinkslinger/ultimate-product-powers`

**Rules:**
- Never commit research files, specs, plans, or synthesis documents here
- Every file in this repo ships to users
- Zero superpowers references anywhere
- All skills must be fully self-contained (no external plugin dependencies)
- Supporting files (prompt templates, reference docs, scripts) live alongside their skill
- v0-sdk is vendored in `scripts/node_modules/` — no user npm install needed

## Plugin Structure

- `.claude-plugin/` — plugin.json + marketplace.json
- `hooks/` — 3 hook scripts (SessionStart, PreToolUse, SubagentStart) + hooks.json + run-hook.cmd
- `skills/` — 14 skills with supporting files
- `agents/` — code-reviewer.md (design-aware)
- `scripts/` — v0-generate.mjs + vendored v0-sdk

## Updating Skills

When a skill is modified in the dev workspace:
1. Copy the updated file(s) to the matching path here
2. Verify zero superpowers references: `grep -ri "superpowers" skills/`
3. Commit + push
4. Users run `/plugin update upp@ultimate-product-powers` to get the update

## Versioning

Current version: **1.0.0**

Three files carry the version — all three must be bumped together on release:
- `.claude-plugin/plugin.json` → `version` field
- `.claude-plugin/marketplace.json` → `metadata.version` AND `plugins[0].version`

**When to bump:**
- **Patch (1.0.x):** Bug fixes, wording tweaks, supporting file updates
- **Minor (1.x.0):** New skills added, existing skills enhanced, hook behavior changes
- **Major (x.0.0):** Breaking changes to skill interfaces, hook output format changes, skill removals

**Release process:**
1. Update all three version fields
2. Update CHANGELOG.md with what changed
3. Commit with message: `release: vX.Y.Z`
4. Tag: `git tag vX.Y.Z && git push --tags`
5. Push: `git push`

Users pick up updates via `/plugin update upp@ultimate-product-powers`.
