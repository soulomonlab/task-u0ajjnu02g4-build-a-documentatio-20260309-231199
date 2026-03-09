QA Runbook — PR Mitigation (429 / DRY_RUN_LIMIT & Pagination Regression)

Purpose
- Provide QA-runbook, automated test stubs, and acceptance criteria to validate mitigation for the PR that introduced pagination regressions and a 429/DRY_RUN_LIMIT issue.

Files created
- output/tests/test_pr_mitigation.py — pytest integration test stubs (skipped unless API_BASE env var is set)
- output/reports/qa_runbook_pr_mitigation.md — this runbook

Scope
- Two priority areas identified by CustomerInsights and Product:
  1) 429 / DRY_RUN_LIMIT behavior: ensure server returns expected status and clients handle Retry-After or error code, and that rate-limiting mitigation is effective.
  2) Pagination migration/regression: ensure pagination API remains backward-compatible and metadata is correct.

Risk areas
- Missing Retry-After header or inconsistent error code across endpoints.
- Inconsistent pagination metadata (page/per_page vs offset/limit), causing SDK/frontend breakage.
- Edge cases for empty pages, very large per_page values, and concurrent requests hitting rate limits.

Test scenarios (MECE)
1) 429 / DRY_RUN_LIMIT
  - S1.1: Server returns 429 + Retry-After header when rate limit exceeded.
  - S1.2: Server returns JSON error with code DRY_RUN_LIMIT when applicable.
  - S1.3: Client retry behavior: respects Retry-After and does exponential backoff. (Automation: integration test + e2e)
  - S1.4: Ensure dry-run mode does not count against real quotas (if applicable).

2) Pagination
  - S2.1: Happy path: page=1, per_page=50 returns <=50 items and meta.page/per_page reflect request.
  - S2.2: Boundary: per_page=1 and per_page=max limits; page beyond last returns empty list and appropriate meta.
  - S2.3: Backward-compat: old SDK queries (e.g., offset/limit or cursor) still supported or documented migration path exists.
  - S2.4: Sorting/stability: repeated requests with same params return deterministic ordering if required.

Acceptance criteria
- Automated tests (integration + unit where possible) cover all scenarios above.
- No P0 regressions found in QA verification run.
- Documentation/Support KB links for 429/DRY_RUN_LIMIT and pagination migration are published and referenced in release notes.
- CI gate: test suite for PR mitigation runs in CI and returns exit code 0 before merging to main.

Automation & running tests
- Tests are written as integration tests that hit API_BASE (environment variable). This avoids false positives in dev environments.
- To run locally (after deployment of a mitigation environment):
  $ export API_BASE="https://staging.api.example.com"
  $ python -m pytest output/tests/test_pr_mitigation.py -v

CI suggestion
- Add a short-lived pipeline job `qa/pr_mitigation` that:
  - Deploys the mitigation build to a staging environment
  - Exposes API_BASE to the CI job
  - Runs pytest for output/tests/test_pr_mitigation.py
  - Fails the job if any tests fail (skipped tests are allowed)

Reporting & triage
- If any test fails, create GitHub issue with severity classification (P0/P1/P2) and include the failing test output.
- P0 failures: notify #ai-backend and #ai-frontend immediately and block release.

Contacts
- QA lead: Dana
- Backend eng: Marcus
- Frontend eng: Kevin
- Support publishing: Chris (already assigned by Product)

Notes
- Tests are integration-focused and intentionally skipped when API_BASE is not set; this prevents CI noise for developers running tests locally without a target environment.

