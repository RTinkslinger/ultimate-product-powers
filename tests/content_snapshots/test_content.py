"""L1: Content snapshot tests — verify required patterns exist in skill/agent files."""

import os
import pytest
from pathlib import Path

from utils.skill_discovery import get_all_skills, get_all_agents, SKILLS_DIR, AGENTS_DIR

MANIFESTS_DIR = Path(__file__).parent / "manifests"


def load_manifest(name: str) -> list[str]:
    """Load required patterns from manifest file."""
    manifest_path = MANIFESTS_DIR / f"{name}.txt"
    if not manifest_path.exists():
        pytest.skip(f"No manifest for {name}")
    with open(manifest_path) as f:
        return [
            line.strip()
            for line in f
            if line.strip() and not line.strip().startswith("#")
        ]


def _skill_manifest_name(skill_dir: str) -> str:
    return skill_dir.replace("-", "_")


@pytest.mark.quick
@pytest.mark.parametrize("skill", get_all_skills())
def test_skill_content_snapshot(skill):
    """Every pattern in the manifest must be present in the SKILL.md."""
    manifest_name = _skill_manifest_name(skill)
    patterns = load_manifest(manifest_name)

    skill_path = os.path.join(SKILLS_DIR, skill, "SKILL.md")
    with open(skill_path) as f:
        content = f.read()

    for pattern in patterns:
        assert pattern in content, (
            f"CONTENT REGRESSION: Required pattern '{pattern}' "
            f"missing from skills/{skill}/SKILL.md"
        )


@pytest.mark.quick
@pytest.mark.parametrize("agent", get_all_agents())
def test_agent_content_snapshot(agent):
    """Every pattern in the manifest must be present in the agent .md file."""
    manifest_name = agent.replace("-", "_")
    patterns = load_manifest(manifest_name)

    agent_path = os.path.join(AGENTS_DIR, f"{agent}.md")
    with open(agent_path) as f:
        content = f.read()

    for pattern in patterns:
        assert pattern in content, (
            f"CONTENT REGRESSION: Required pattern '{pattern}' "
            f"missing from agents/{agent}.md"
        )
