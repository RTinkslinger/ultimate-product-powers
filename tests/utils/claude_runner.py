"""Wraps `claude -p` invocation with timeout and fresh-session isolation."""

import subprocess
import json
import os
from pathlib import Path

from .skill_discovery import UPP_PLUGIN_DIR


def claude_run(
    prompt: str,
    *,
    max_turns: int = 3,
    timeout: int = 300,
    no_skills: bool = False,
    plugin_dir: str | None = None,
) -> list[dict]:
    """Run claude -p and return parsed stream-json events.

    Args:
        prompt: The prompt to send
        max_turns: Maximum conversation turns
        timeout: Subprocess timeout in seconds
        no_skills: If True, point --plugin-dir to an empty dir (no skills loaded)
        plugin_dir: Plugin directory (defaults to UPP repo root)

    Returns:
        List of parsed JSON event dicts from stream-json output
    """
    cmd = [
        "claude", "-p", prompt,
        "--output-format", "stream-json",
        "--dangerously-skip-permissions",
        "--max-turns", str(max_turns),
        "--verbose",
    ]

    if no_skills:
        empty_dir = os.path.join(os.path.dirname(__file__), "..", "_empty_plugin")
        os.makedirs(empty_dir, exist_ok=True)
        cmd.extend(["--plugin-dir", empty_dir])
    else:
        cmd.extend(["--plugin-dir", plugin_dir or UPP_PLUGIN_DIR])

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=UPP_PLUGIN_DIR,
    )

    events = []
    for line in result.stdout.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue

    return events
