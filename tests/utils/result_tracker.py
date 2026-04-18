"""Save test results per release tag for version-over-version tracking."""

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

RESULTS_DIR = Path(__file__).parent.parent / "test-results"


def get_current_tag() -> str:
    """Get the current git tag or commit SHA."""
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--exact-match"],
            capture_output=True, text=True,
            cwd=str(Path(__file__).parent.parent.parent),
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass

    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True,
            cwd=str(Path(__file__).parent.parent.parent),
        )
        return result.stdout.strip()
    except Exception:
        return "unknown"


def save_results(
    passed: int, failed: int, errors: int, details: dict | None = None
):
    """Save test results snapshot for the current release."""
    RESULTS_DIR.mkdir(exist_ok=True)
    tag = get_current_tag()

    result = {
        "tag": tag,
        "timestamp": datetime.now().isoformat(),
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "details": details or {},
    }

    output_path = RESULTS_DIR / f"{tag}.json"
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
