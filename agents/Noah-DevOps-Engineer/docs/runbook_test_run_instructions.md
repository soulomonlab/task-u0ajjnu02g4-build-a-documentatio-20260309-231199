Runbook Validation — DevOps Execution Instructions

Purpose
- Provide exact commands and CI steps for DevOps to install and execute the pytest-based runbook validation tests created by QA (Dana).

Preconditions
- Repo is checked out and up-to-date with the branch containing output/tests/test_runbook_validation.py.
- Access to staging environment where runbook docs are published. If runbooks are stored in the repo under output/docs/, tests will run against those local files. If published to a staging URL, update TEST_TARGET_URL below.

Commands (local)
1. Create virtualenv (optional but recommended):
   python -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   .venv\Scripts\activate    # Windows
2. Install test runner:
   python -m pip install --upgrade pip
   python -m pip install pytest pytest-cov
3. Run tests:
   python -m pytest output/tests/test_runbook_validation.py -q

Commands (CI)
- There's a GitHub Actions workflow at .github/workflows/run_runbook_tests.yml which installs pytest and runs the single test file. Trigger with workflow_dispatch or push changes to output/tests/.

Staging URL
- If runbooks are published to staging, set TEST_TARGET_URL env var before running tests, e.g.:
  export TEST_TARGET_URL=https://staging.docs.example.com
  python -m pytest output/tests/test_runbook_validation.py -q

Artifacts
- The GitHub Action will upload test artifacts from output/tests/ as runbook-test-output; review those for logs and failures.

Next steps for DevOps
1. Run the local commands above or trigger the GitHub Actions workflow.
2. Share stdout/stderr of pytest run and the uploaded artifact from the Action.
3. If tests need additional Python deps to access external staging URLs (e.g., requests), add them to the workflow install step.
