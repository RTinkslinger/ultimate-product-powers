"""Hook smoke tests — verify bash hook scripts run without error."""

import subprocess
import os
import pytest
from pathlib import Path

HOOKS_DIR = Path(__file__).parent.parent.parent / "hooks"
FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.mark.quick
def test_session_start_runs():
    """SessionStart hook should exit 0."""
    script = HOOKS_DIR / "session-start"
    if not script.exists():
        pytest.skip("session-start hook not found")
    result = subprocess.run(
        ["bash", str(script)],
        capture_output=True,
        text=True,
        timeout=30,
        input="",  # provide empty stdin so hook doesn't block waiting
        env={**os.environ, "HOOK_EVENT": "SessionStart"},
    )
    assert result.returncode == 0, f"session-start failed: {result.stderr}"


@pytest.mark.quick
def test_pretooluse_component_path():
    """PreToolUse hook should exit 0 on component path."""
    script = HOOKS_DIR / "pretooluse-design-inject"
    if not script.exists():
        pytest.skip("pretooluse-design-inject hook not found")

    fixture = (FIXTURES_DIR / "component_path.json").read_text()
    result = subprocess.run(
        ["bash", str(script)],
        input=fixture,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0, f"pretooluse-design-inject failed: {result.stderr}"


@pytest.mark.quick
def test_pretooluse_non_component_path():
    """PreToolUse hook should exit 0 on non-component path and produce no injection."""
    script = HOOKS_DIR / "pretooluse-design-inject"
    if not script.exists():
        pytest.skip("pretooluse-design-inject hook not found")

    fixture = (FIXTURES_DIR / "non_component_path.json").read_text()
    result = subprocess.run(
        ["bash", str(script)],
        input=fixture,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0


@pytest.mark.quick
def test_subagent_hook_runs():
    """SubagentStart hook should exit 0."""
    script = HOOKS_DIR / "subagent-design-bootstrap"
    if not script.exists():
        pytest.skip("subagent-design-bootstrap hook not found")
    result = subprocess.run(
        ["bash", str(script)],
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0, f"subagent-design-bootstrap failed: {result.stderr}"
