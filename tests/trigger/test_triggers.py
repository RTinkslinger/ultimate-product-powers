"""L2: Trigger tests — verify correct skill fires for each prompt."""

import json
import os
import pytest
from pathlib import Path

from utils.claude_runner import claude_run
from utils.stream_parser import extract_skill_invocations, check_premature_action

PROMPTS_DIR = Path(__file__).parent / "prompts"
EXPECTED_PATH = Path(__file__).parent / "expected.json"

with open(EXPECTED_PATH) as f:
    EXPECTED = json.load(f)


def get_prompt_files() -> list[str]:
    """Discover all prompt files."""
    return sorted([f for f in os.listdir(PROMPTS_DIR) if f.endswith(".txt")])


@pytest.mark.quick
@pytest.mark.timeout(120)
@pytest.mark.parametrize("prompt_file", get_prompt_files())
def test_skill_trigger(prompt_file):
    """Assert the expected skill fires (or doesn't fire for negatives)."""
    prompt_path = PROMPTS_DIR / prompt_file
    prompt = prompt_path.read_text().strip()

    expected = EXPECTED[prompt_file]
    expected_skill = expected["skill"]
    prompt_type = expected["type"]
    should_trigger = expected.get("should_trigger", True)

    events = claude_run(prompt, max_turns=3)
    skills = extract_skill_invocations(events)
    skill_names = [s.skill_name for s in skills]

    if not should_trigger:
        # Negative test: skill should NOT appear
        assert expected_skill not in skill_names, (
            f"NEGATIVE TRIGGER FAILURE: '{expected_skill}' fired on negative "
            f"prompt '{prompt_file}' — skill description may be too broad"
        )
        return

    # Positive test: skill should appear
    if expected_skill in skill_names:
        # Check premature action for explicit requests
        if prompt_type == "explicit":
            premature = check_premature_action(events, skills)
            assert not premature, (
                f"PREMATURE ACTION: {premature} fired before Skill tool on "
                f"explicit request '{prompt_file}'"
            )
        return

    # Retry once (strict + retry)
    events = claude_run(prompt, max_turns=3)
    skills = extract_skill_invocations(events)
    skill_names = [s.skill_name for s in skills]

    assert expected_skill in skill_names, (
        f"TRIGGER REGRESSION: Prompt '{prompt_file}' expected skill "
        f"'{expected_skill}' but got: {skill_names} (after retry)"
    )
