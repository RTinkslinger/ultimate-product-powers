"""Shared pytest fixtures for UPP test suite.

Shared functions (get_all_skills, get_all_agents, SKILLS_DIR, AGENTS_DIR)
live in utils/skill_discovery.py — import from there, NOT from this file.
conftest.py only contains fixtures.
"""

import os
import pytest

from utils.claude_runner import claude_run
from utils.skill_discovery import SKILLS_DIR, AGENTS_DIR
from utils.result_tracker import save_results


@pytest.fixture
def run_claude():
    """Fixture wrapping claude_run for test use."""
    return claude_run


@pytest.fixture
def skill_content():
    """Read a skill's SKILL.md content."""
    def _read(skill_name: str) -> str:
        path = os.path.join(SKILLS_DIR, skill_name, "SKILL.md")
        with open(path) as f:
            return f.read()
    return _read


@pytest.fixture
def agent_content():
    """Read an agent's .md content."""
    def _read(agent_name: str) -> str:
        path = os.path.join(AGENTS_DIR, f"{agent_name}.md")
        with open(path) as f:
            return f.read()
    return _read


def pytest_sessionfinish(session, exitstatus):
    """Auto-save test results on session completion."""
    passed = session.testscollected - session.testsfailed
    try:
        save_results(
            passed=passed,
            failed=session.testsfailed,
            errors=0,
            details={"exit_status": exitstatus},
        )
    except Exception:
        pass  # Don't fail the session on tracking errors
