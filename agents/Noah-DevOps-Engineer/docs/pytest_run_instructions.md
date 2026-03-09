DevOps instructions: Running Dana's pytest against staging docs

Purpose
- Execute output/tests/test_runbook_validation.py (Dana) against the staging documentation snapshot and return full test logs.

Assumptions
- Python 3.11+ available on runner (local VM or CI).
- The repository contains the staging docs under output/docs/staging/ or accessible by URL (replace STAGING_DOCS_URL below).
- Tests live at output/tests/test_runbook_validation.py (already provided by Dana).

Commands (one-off run)
1) Confirm staging docs location:
   - Option A: Repo path (e.g., output/docs/staging/) — set STAGING_DOCS_PATH variable.
   - Option B: Public staging URL (e.g., https://staging.example.com/docs) — set STAGING_DOCS_URL variable.

2) Install test deps and run tests:
   python -m pip install --upgrade pip
   python -m pip install pytest pytest-cov
   python -m pytest output/tests/test_runbook_validation.py -q

CI job (GitHub Actions snippet)
- Use ubuntu-latest runner with python-version 3.11.
- Persist test logs as artifact for review.

Expected output
- Full pytest log (stdout + stderr). Save as artifact or attach to issue/task.

If tests fail
- Tag @Dana (#ai-qa) with the test summary and full logs.

Notes for whoever runs this (DevOps)
- If running on staging VM, run the commands in a virtualenv or ephemeral container.
- If running in CI, attach logs and artifacts and mark task as done.

Placeholders to fill before running:
- STAGING_DOCS_URL: <paste staging docs URL here if using web endpoint>
- STAGING_DOCS_PATH: <repo path to staging docs if using repo snapshot>

Files created by this run (automatically):
- output/config/run_pytests.sh  -> execution script
- output/reports/pytest_run_137_log.txt -> full test run logs (created after run)
