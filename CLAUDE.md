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
3. Bump version in `.claude-plugin/plugin.json` if releasing
4. Commit + push
5. Users run `/plugin update upp@ultimate-product-powers` to get the update
