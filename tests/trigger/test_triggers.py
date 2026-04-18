"""L2: Trigger tests — verify correct skill fires for each prompt.

IMPORTANT: All L2 tests are xfail(strict=False). Headless mode routing is
inherently probabilistic — the model sometimes answers directly without
invoking any skill, and the using-upp "1% = invoke" rule causes over-invocation
on negative prompts. L2 measures routing quality over time; it does NOT gate
pushes. L1 content snapshots are the gating regression tests.

Test types:
- explicit: User names the skill directly. Should pass ~80%+ of the time.
- negative: Unrelated prompt. Skill should NOT fire. ~70%+ with good prompts.
- naive: Natural language. Model routing quality indicator. ~10-20%.
- keyword-absent: Conceptual match. Model routing quality indicator. ~15-25%.

An unexpected pass (xpass) is logged and welcome — it means routing worked.
"""

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


@pytest.mark.full
@pytest.mark.timeout(120)
@pytest.mark.parametrize("prompt_file", get_prompt_files())
def test_skill_trigger(prompt_file, request):
    """Assert the expected skill fires (or doesn't fire for negatives)."""
    prompt_path = PROMPTS_DIR / prompt_file
    prompt = prompt_path.read_text().strip()

    expected = EXPECTED[prompt_file]
    expected_skill = expected["skill"]
    prompt_type = expected["type"]
    should_trigger = expected.get("should_trigger", True)

    # All L2 tests are xfail — headless routing is probabilistic
    request.node.add_marker(pytest.mark.xfail(
        strict=False,
        reason="Headless routing is probabilistic — L2 measures quality, not correctness",
    ))

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
