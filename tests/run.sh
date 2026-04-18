#!/usr/bin/env bash
# UPP Test Runner — creates venv, installs deps, runs pytest
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Create venv if not exists
if [ ! -d ".venv" ]; then
    echo "Creating test venv..."
    python3 -m venv .venv
    .venv/bin/pip install -r requirements.txt -q
fi

# Activate and run
source .venv/bin/activate

echo "========================================"
echo " UPP Test Suite"
echo "========================================"
echo "Plugin dir: $(cd .. && pwd)"
echo "Python: $(python3 --version)"
echo "Pytest: $(pytest --version 2>/dev/null | head -1)"
echo ""

# Pass all args to pytest
pytest "$@"
