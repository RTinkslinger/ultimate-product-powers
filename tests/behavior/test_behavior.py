"""L3: Behavior RED-GREEN tests for 6 core skills.

For each skill, run the SAME task in two modes:
- RED: --bare (no plugins, hooks, or CLAUDE.md)
- GREEN: --plugin-dir UPP (skill loaded)

Assert: GREEN contains at least ONE marker from a candidate set that
RED does NOT contain. Uses any-of matching because LLM output vocabulary
varies per run — the CONCEPT is consistent, the WORDS are not.

NOTE: L3 tests are xfail(strict=False). Headless mode routing is
probabilistic — the model often completes the task directly without
invoking skills, so GREEN output may lack skill-specific vocabulary.
Tests that do pass (xpass) validate that the skill genuinely changes behavior.
"""

import json
import pytest
from pathlib import Path

from utils.claude_runner import claude_run
from utils.stream_parser import extract_all_text

MARKERS_PATH = Path(__file__).parent / "markers.json"
TASKS_DIR = Path(__file__).parent / "tasks"

with open(MARKERS_PATH) as f:
    MARKERS = json.load(f)


@pytest.mark.full
@pytest.mark.timeout(600)
@pytest.mark.xfail(strict=False, reason="Headless routing is probabilistic — skill may not be invoked")
@pytest.mark.parametrize("skill_name", list(MARKERS.keys()))
def test_behavior_red_green(skill_name):
    """GREEN must produce at least one marker that RED does not."""
    config = MARKERS[skill_name]
    task_path = TASKS_DIR / config["task_file"]
    prompt = task_path.read_text().strip()
    green_markers = config["green_markers"]

    # RED run: empty plugin dir (no skills)
    red_events = claude_run(prompt, max_turns=5, no_skills=True)
    red_text = extract_all_text(red_events).lower()

    # GREEN run: with UPP plugin
    green_events = claude_run(prompt, max_turns=5)
    green_text = extract_all_text(green_events).lower()

    # Find which markers appear in GREEN
    green_hits = [m for m in green_markers if m.lower() in green_text]

    # At least ONE marker must appear in GREEN
    assert len(green_hits) > 0, (
        f"GREEN MISSING ALL MARKERS: None of {green_markers} found in "
        f"GREEN output for skill '{skill_name}'. The skill may not be "
        f"loading or the markers are wrong."
    )

    # At least ONE marker that's in GREEN must be ABSENT from RED
    green_only = [m for m in green_hits if m.lower() not in red_text]
    assert len(green_only) > 0, (
        f"RED-GREEN INDISTINGUISHABLE: Every marker found in GREEN was "
        f"also in RED for skill '{skill_name}'. GREEN hits: {green_hits}. "
        f"The skill may not be adding behavioral value beyond training data."
    )
