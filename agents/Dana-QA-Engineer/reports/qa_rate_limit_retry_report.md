QA Run: Rate Limit & Retry Tests

Scope:
- Run k6 load test per instructions in output/docs/qa_run_instructions.md
- Run pytest suite for integration checks against staging
- Collect artifacts: k6 summary, k6-result.json, pytest results (JUnit XML), system logs, telemetry (error rates, p95 latency, CPU/mem)

Acceptance Criteria (from runbook):
- Sustained 60 RPM (requests per minute) with burst to 10x (600 RPM) tolerated for short windows
- Error rate < 1% during steady-state
- No P1 incidents (crash, data loss, security breach)

Test Results Summary:
- pytest: NOT RUN YET. Tests are present at output/tests/test_rate_limit_retry.py and require STAGING_URL env var.
- k6: NOT RUN YET. k6 script referenced in runbook.

Artifacts to attach after execution:
- pytest JUnit XML: output/reports/junit_pytest_results.xml
- pytest console log: output/reports/pytest_console.log
- k6 summary: output/reports/k6_summary.txt
- k6 JSON: output/reports/k6_result.json
- Telemetry snapshots: output/reports/telemetry_YYYYMMDD.json

Next steps:
1) Run pytest and k6 per runbook (output/docs/qa_run_instructions.md). Ensure STAGING_URL, K6_SCRIPT_PATH, and credentials are set.
2) Attach artifacts to this report path.
3) Coordinate 2-week canary schedule with Marcus: propose start date, rolling percentage, rollback triggers.

