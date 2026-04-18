"""L3: Behavior RED-GREEN tests for 6 core skills.

For each skill, run the SAME task in two modes:
- RED: --plugin-dir empty (no skills loaded)
- GREEN: --plugin-dir UPP (skill loaded)

Assert: GREEN contains structural markers that RED does NOT.
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
@pytest.mark.timeout(300)
@pytest.mark.parametrize("skill_name", list(MARKERS.keys()))
def test_behavior_red_green(skill_name):
    """GREEN must produce markers that RED does not."""
    config = MARKERS[skill_name]
    task_path = TASKS_DIR / config["task_file"]
    prompt = task_path.read_text().strip()
    green_markers = config["green_markers"]

    # RED run: empty plugin dir (no skills)
    red_events = claude_run(prompt, max_turns=5, no_skills=True)
    red_text = extract_all_text(red_events)

    # GREEN run: with UPP plugin
    green_events = claude_run(prompt, max_turns=5)
    green_text = extract_all_text(green_events)

    # Assert: each marker present in GREEN
    for marker in green_markers:
        assert marker.lower() in green_text.lower(), (
            f"GREEN MISSING MARKER: '{marker}' not found in GREEN output "
            f"for skill '{skill_name}'"
        )

    # Assert: at least ONE marker absent in RED (proves skill influence)
    red_absent = [m for m in green_markers if m.lower() not in red_text.lower()]
    assert len(red_absent) > 0, (
        f"RED-GREEN INDISTINGUISHABLE: All markers found in BOTH RED and "
        f"GREEN for skill '{skill_name}'. The markers may be in Claude's "
        f"training data rather than from the skill. Markers: {green_markers}"
    )
