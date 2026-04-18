"""Shared skill/agent discovery functions. Import from here, not conftest."""

import os
from pathlib import Path

UPP_PLUGIN_DIR = str(Path(__file__).parent.parent.parent)
SKILLS_DIR = os.path.join(UPP_PLUGIN_DIR, "skills")
AGENTS_DIR = os.path.join(UPP_PLUGIN_DIR, "agents")


def get_all_skills() -> list[str]:
    """Discover all skill directories."""
    return sorted([
        d for d in os.listdir(SKILLS_DIR)
        if os.path.isfile(os.path.join(SKILLS_DIR, d, "SKILL.md"))
    ])


def get_all_agents() -> list[str]:
    """Discover all agent files."""
    return sorted([
        f.replace(".md", "") for f in os.listdir(AGENTS_DIR)
        if f.endswith(".md")
    ])
