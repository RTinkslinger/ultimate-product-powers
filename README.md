# Ultimate Product Powers (UPP)

Design-aware product development skills for Claude Code.

## What's Included

**Core pipeline:** brainstorming (prototype-first) → writing-plans (design-aware) → executing-plans (three-gate review)

**Companion skills:** product-redesign, design-system-enforcer, agentic-ux-patterns

**Design enforcement:** Automatic via hooks — SessionStart detects DESIGN.md, PreToolUse injects design tokens on component files, SubagentStart bootstraps subagents with token context.

**Agent:** Design-aware code reviewer

## Setup

### 1. Install the plugin

Add to `~/.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "upp": {
      "source": { "source": "github", "repo": "<org>/ultimate-product-powers" }
    }
  },
  "enabledPlugins": { "upp@upp": true }
}
```

### 2. Install v0 wrapper dependencies

```bash
cd <plugin-root>/scripts && npm install
```

Required for prototype generation during brainstorming.

### 3. Configure MCP integrations (optional)

These enhance the brainstorming pipeline but are not required:

```bash
# Figma MCP (design extraction + drift detection)
claude mcp add --scope user --transport http figma https://mcp.figma.com/mcp

# Google Stitch MCP (mood exploration + design system generation)
claude mcp add --scope user --transport http stitch https://stitch.googleapis.com/mcp --header "X-Goog-Api-Key: YOUR_KEY"
```

v0 API key: set `V0_API_KEY` in your shell profile (`~/.zshrc` or `~/.bashrc`).

## Skills

| Skill | Purpose |
|-------|---------|
| brainstorming | Turn ideas into designs + specs. Prototype-first for greenfield frontend. |
| writing-plans | Create implementation plans from specs. Design-aware ordering + verification. |
| executing-plans | Execute plans via subagents or inline. Three-gate review (spec + quality + design). |
| product-redesign | Overhaul existing frontend design systems. |
| design-system-enforcer | Enforce DESIGN.md during implementation. Auto via hooks. |
| agentic-ux-patterns | Reference for streaming, approvals, errors in agent UIs. |
| using-upp | Skill discovery guide (auto-injected at session start). |

## How It Works

1. **Brainstorming** discovers the problem, generates prototypes (v0 + Stitch), produces DESIGN.md and a spec
2. **Writing-plans** reads the spec and creates a design-aware implementation plan with progressive verification
3. **Executing-plans** dispatches subagents per task, reviews each (spec → quality → design compliance), verifies golden samples
4. **Hooks** enforce design tokens at every step — session start, file writes, subagent dispatch

## License

MIT
