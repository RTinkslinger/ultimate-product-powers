---
name: agentic-ux-patterns
description: >
  Reference patterns for agentic product UX — streaming strategies, approval flows,
  error recovery, accessibility for streaming content, responsive agent UI.
  Use when brainstorming discovers an agentic product (agent output, JSON render,
  streaming UI), or when building frontend components that handle agent output.
  Triggers on: "streaming UI", "agent response", "tool call visualization",
  "approval flow", "error recovery for agent", "build agent interface",
  or any frontend task involving agent-produced dynamic content.
---

# Agentic UX Patterns

You're building UI for an AI agent's output. This isn't a normal frontend — the content is dynamic, arrives over time, and can fail mid-stream. These patterns are the difference between a polished agentic product and a chat wrapper with a spinner.

This is a reference skill — expertise you consult, not a workflow you follow. Your project's DESIGN.md Section 10 defines WHAT the agent produces (component registry, types, props). This skill covers HOW it should behave at runtime.

## Streaming Strategies

Not all streaming is "append tokens to a string." Pick the strategy that matches your content type.

| Strategy | How It Works | Best For | Watch Out |
|----------|-------------|----------|-----------|
| **Token-by-token** | Append each token, re-render the growing string | Simple text responses | Layout thrash with markdown — unclosed bold tags, code fences cause flicker |
| **Chunk streaming** | Batch tokens into semantic chunks (sentences, paragraphs) | Mixed content (text + structured) | Slightly higher perceived latency, but smoother rendering |
| **Skeleton-then-replace** | Show placeholder skeleton matching expected layout, swap with final content | Tables, charts, structured data | Jarring if skeleton differs significantly from final. Match the shape. |
| **Event-based semantic** | Typed events (TextDelta, ToolCallDelta, StructuredObject) | Complex agent workflows with tool calls | More implementation work. Use Vercel AI SDK's data streams or OpenAI's Response events |

**Partial markdown handling:** Streaming markdown creates XSS risk and visual instability if you naively set `innerHTML`. Use a DOM sanitizer (DOMPurify) with a streaming markdown parser that APPENDS nodes rather than replacing the entire container. Never render unclosed HTML tags mid-stream.

**Structured output during streaming:** For JSON/structured data arriving progressively, keep schemas flat. Deep nesting + partial arrival = broken renders. Render fields as they arrive — show title before description before table, each appearing as it completes.

## Approval Flow Taxonomy

When the agent takes actions (writes files, calls APIs, modifies data), the user needs control. Match the approval pattern to the action's blast radius.

| Pattern | When to Use | Risk Level |
|---------|------------|------------|
| **Accept All / Reject All** | Low-risk batch changes (format 5 files, rename variables) | Low |
| **Review Each** | High-risk or mixed changes (some safe, some destructive) | High |
| **Intent Preview** | Destructive actions ("I will delete 3 files and modify 2. Proceed?") | Critical |
| **Diff View** | Code modifications — side-by-side or inline diff with accept/reject per hunk | Medium-High |
| **Confirmation Dialog** | Irreversible actions — modal with "I understand this cannot be undone" | Critical |
| **Auto-approve with audit** | Trusted, low-risk actions — log everything, surface undo option | Low |

The key tension: too many approval prompts → user enables "accept all" and stops reading. Too few → user loses trust after a destructive action. Calibrate by blast radius: auto-approve reads, review writes, require confirmation for deletes.

## Error Recovery

Agent failures are not exceptional — they're routine. Design for them as a first-class state.

**Principles:**
- **Preserve partial output.** Never discard what was already generated. Show it with an error banner below.
- **Recoverable vs fatal.** Recoverable errors (network, rate limit) get retry buttons. Fatal errors (model refusal, context exceeded) get clear explanation and alternative actions.
- **Progress context.** "Failed at step 3 of 5" is actionable. "Error occurred" is not.
- **Exponential backoff for rate limits.** Don't hammer a 429. Show a countdown timer.
- **Action Audit & Undo.** For agentic systems, maintain a chronological log of agent-initiated actions with a visible Undo button. Trust requires a safety net.

| Error Type | UX Pattern | User Action |
|-----------|-----------|------------|
| Partial response failure | Show what was generated + error banner | Retry (continues from last good state) or regenerate fully |
| Rate limiting | Countdown timer or queue position | Wait, or switch to different model |
| Context window exceeded | Warning with context usage indicator | Start new conversation or summarize |
| Tool execution failure | Inline error in tool call accordion | Retry tool call, skip, or provide manual input |
| Network error | Toast notification with retry button | Retry request |
| Model refusal | Explanation with suggestion to rephrase | Edit and resubmit |

## Streaming Accessibility

Streaming content is an accessibility minefield. Screen readers can't handle 30 updates per second. These aren't nice-to-haves — they're requirements.

**ARIA live regions:**
- Wrap the message container in `aria-live="polite"` — announces new content when user is idle, doesn't interrupt
- Set `aria-atomic="false"` — reads only NEW tokens, not the entire message on each update
- **Debounce updates to ~500ms.** Without this, screen readers announce every token and become unusable

**Focus management:**
- When response completes, focus STAYS on the input field. Users want to send immediate follow-ups — don't steal focus to the response
- Tool call accordions must be expandable via keyboard (Enter to toggle, Tab to navigate between)
- Code blocks need keyboard-accessible copy buttons
- All interactive elements in agent output (citations, feedback buttons) must be Tab-navigable

**Reduced motion (`prefers-reduced-motion`):**
- Replace token-by-token streaming animation with instant text appearance
- Replace thinking indicator animations with static "Thinking..." text
- Replace slide-in transitions with instant appearance
- Keep focus indicators visible — never remove `outline`

## Responsive Agent UI

Agent interfaces have unique responsive challenges — sidebars, artifacts, streaming content, tool call details all need mobile adaptations.

| Component | Desktop | Tablet | Mobile |
|-----------|---------|--------|--------|
| **Sidebar** (chat history, config) | Persistent, resizable | Collapsible overlay | Hidden behind hamburger |
| **Artifacts / Canvas** | Side-by-side with chat | Full-width overlay | Full-screen modal |
| **Input area** | Fixed bottom, multiline | Fixed bottom, multiline | Sticky, auto-expanding |
| **Code blocks** | Full-width with line numbers | Full-width, horizontal scroll | Full-width, horizontal scroll |
| **Tool call details** | Inline accordion | Inline accordion | Bottom sheet |
| **File attachments** | Drag-and-drop + button | Button | Native file picker + camera |

**Input area design:**
- Auto-expanding textarea that grows with content, collapses on send
- Attachment bar: file, image, voice input options
- Model selector: dropdown or pill selector above input (if multiple models available)
- Send button: always visible, changes state when content is entered
- Keyboard: Cmd+Enter to send, Shift+Enter for newline

## Content Type Hierarchy

When agent output contains mixed types, render them in this order of visual weight:

1. **Block-level** — code blocks, tables, charts, images, action cards. Full width, card elevation to distinguish from prose.
2. **Inline** — citations, status badges, small indicators, links. Flow with surrounding text, no visual disruption.
3. **Interactive** — buttons, forms, approval cards, file selectors. Highlighted and prominent — the user needs to act on these.
4. **Meta** — thinking traces, tool call logs, debug information. Collapsible by default, de-emphasized visually. Power users expand; most users never see.

Vertical stacking is the default layout. Card elevation separates structured data (tables, charts) from prose. Adjacent same-type blocks merge (consecutive code in the same language → one block). Section grouping ties related content (explanation + code + output).

## Thinking & Reasoning Indicators

How to show the user that the agent is working — pick based on how much reasoning visibility serves the user.

| Pattern | Visual | When to Use |
|---------|--------|------------|
| **Pulsing dots** | Three animated dots | Simple responses, no tool use. Universal and familiar. |
| **Thinking blocks** | Collapsible section showing reasoning trace | Complex reasoning where transparency builds trust. Claude's extended thinking. |
| **Step indicators** | Sequential steps with checkmarks | Deterministic multi-step workflows. Users see progress through known stages. |
| **Tool call pills** | Inline indicators: "Searching web...", "Reading file..." | Agent using tools. Shows WHAT it's doing, not just THAT it's doing something. |

More visibility → more trust but more visual noise. Default to tool call pills for agentic products (users care what the agent is doing). Add thinking blocks only when reasoning transparency is a product value.
