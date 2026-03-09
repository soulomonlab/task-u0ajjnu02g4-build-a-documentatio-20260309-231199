#!/usr/bin/env bash
# Execution script for running Dana's pytest against staging docs (task #137)
# Usage: ./output/config/run_pytests.sh [--staging-path PATH] [--staging-url URL]

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${SCRIPT_DIR%/output/config}"
TEST_FILE="output/tests/test_runbook_validation.py"

STAGING_PATH=""
STAGING_URL=""

while [[ "$#" -gt 0 ]]; do
  case $1 in
    --staging-path) STAGING_PATH="$2"; shift 2;;
    --staging-url) STAGING_URL="$2"; shift 2;;
    -h|--help) echo "Usage: $0 [--staging-path PATH] [--staging-url URL]"; exit 0;;
    *) echo "Unknown arg: $1"; exit 1;;
  esac
done

if [[ -z "$STAGING_PATH" && -z "$STAGING_URL" ]]; then
  echo "ERROR: must provide --staging-path or --staging-url"
  exit 2
fi

# Create virtualenv
PYTHON_BIN="python3.11"
if ! command -v $PYTHON_BIN >/dev/null 2>&1; then
  PYTHON_BIN="python"
fi

$PYTHON_BIN -m pip install --upgrade pip
$PYTHON_BIN -m pip install virtualenv
$PYTHON_BIN -m virtualenv .venv
source .venv/bin/activate

pip install pytest pytest-cov

# If STAGING_URL provided, export environment variable for tests to pick up
if [[ -n "$STAGING_URL" ]]; then
  export STAGING_DOCS_URL="$STAGING_URL"
fi
if [[ -n "$STAGING_PATH" ]]; then
  export STAGING_DOCS_PATH="$STAGING_PATH"
fi

# Run tests and capture full logs
LOG_FILE="${REPO_ROOT}output/reports/pytest_run_137_log.txt"
mkdir -p "$(dirname "$LOG_FILE")"

pytest -q "$TEST_FILE" 2>&1 | tee "$LOG_FILE"
EXIT_CODE=${PIPESTATUS[0]}

echo "Test exit code: $EXIT_CODE" | tee -a "$LOG_FILE"

exit $EXIT_CODE
