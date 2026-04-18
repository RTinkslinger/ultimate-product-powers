"""Parse stream-json events for Skill tool invocations and tool call ordering.

EVENT SCHEMA (verified 2026-04-18 from prototype step):

Event types: system, assistant, user, rate_limit_event, result

Skill tool invocation path:
  event["type"] == "assistant"
  event["message"]["content"] → list of blocks
  block["type"] == "tool_use"
  block["name"] == "Skill"
  block["input"]["skill"] == "upp:security-review"  ← includes plugin namespace

Tool result path:
  event["type"] == "user"
  event["message"]["content"][N]["type"] == "tool_result"
  event["message"]["content"][N]["tool_use_id"] → matches block["id"]
"""

from dataclasses import dataclass


class StreamFormatChanged(Exception):
    """Raised when stream-json format differs from expected schema."""
    pass


@dataclass
class SkillInvocation:
    skill_name: str
    raw_skill_name: str  # includes namespace prefix
    event_index: int


@dataclass
class ToolCall:
    tool_name: str
    event_index: int


def _get_content_blocks(event: dict) -> list[dict]:
    """Extract content blocks from a stream-json event.

    Verified path: event.message.content (list of blocks).
    Raises StreamFormatChanged if structure doesn't match expected schema.
    """
    if event.get("type") not in ("assistant", "user"):
        return []

    message = event.get("message")
    if not isinstance(message, dict):
        return []

    content = message.get("content")
    if content is None:
        return []

    if isinstance(content, list):
        return content

    # If content is present but not a list, format has changed
    if isinstance(content, str):
        # Text-only response, no tool blocks — this is normal
        return []

    raise StreamFormatChanged(
        f"event.message.content is {type(content).__name__}, expected list. "
        "The stream-json format may have changed."
    )


def _strip_namespace(raw_skill: str) -> str:
    """Strip plugin namespace prefix: 'upp:security-review' → 'security-review'."""
    if ":" in raw_skill:
        return raw_skill.split(":", 1)[1]
    return raw_skill


def extract_skill_invocations(events: list[dict]) -> list[SkillInvocation]:
    """Extract all Skill tool invocations from stream-json events."""
    skills = []
    found_any_tool_use = False

    for i, event in enumerate(events):
        for block in _get_content_blocks(event):
            if block.get("type") == "tool_use":
                found_any_tool_use = True
                if block.get("name") == "Skill":
                    raw = block.get("input", {}).get("skill", "")
                    if raw:
                        skills.append(SkillInvocation(
                            skill_name=_strip_namespace(raw),
                            raw_skill_name=raw,
                            event_index=i,
                        ))

    # Format change detection
    if len(events) > 10 and not found_any_tool_use:
        # Check if there ARE assistant events (if none, session was too short)
        assistant_count = sum(1 for e in events if e.get("type") == "assistant")
        if assistant_count > 1:
            raise StreamFormatChanged(
                f"Parsed {len(events)} events ({assistant_count} assistant) "
                "but found zero tool_use blocks. "
                "Re-run prototype step to verify stream-json format."
            )

    return skills


def extract_tool_calls(events: list[dict]) -> list[ToolCall]:
    """Extract all tool calls (any tool, not just Skill) from stream events."""
    tools = []
    for i, event in enumerate(events):
        for block in _get_content_blocks(event):
            if block.get("type") == "tool_use":
                tools.append(ToolCall(
                    tool_name=block.get("name", ""),
                    event_index=i,
                ))
    return tools


def check_premature_action(
    events: list[dict], skills: list[SkillInvocation]
) -> list[str]:
    """Check if Write/Edit/Bash tools fired before the first Skill tool.

    Returns list of premature tool names (empty = clean).
    Only meaningful for explicit-request prompts.
    """
    if not skills:
        return []

    first_skill_index = skills[0].event_index
    all_tools = extract_tool_calls(events)

    premature = []
    for tool in all_tools:
        if tool.event_index >= first_skill_index:
            break
        if tool.tool_name in ("Write", "Edit", "Bash"):
            premature.append(tool.tool_name)

    return premature


def extract_all_text(events: list[dict]) -> str:
    """Concatenate all text content from stream events."""
    texts = []
    for event in events:
        for block in _get_content_blocks(event):
            if block.get("type") == "text":
                texts.append(block.get("text", ""))
    return "\n".join(texts)
