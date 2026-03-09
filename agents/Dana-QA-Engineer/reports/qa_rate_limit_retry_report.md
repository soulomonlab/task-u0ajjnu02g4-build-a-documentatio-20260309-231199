QA Rate Limit & Retry Report

Run summary (attempted locally in CI runner):

1) Pytest run
- Command attempted: python -m pytest output/tests/tests_retry_behavior_pytest.py -q --junitxml=output/reports/pytest_results.xml
- Result: FAILED to run pytest due to missing pytest module.
- stderr:
  Could not find platform independent libraries <prefix>
  C:\Python313\python.exe: No module named pytest
- Outcome: No pytest XML produced (output/reports/pytest_results.xml not created). The pytest test file exists at output/tests/tests_retry_behavior_pytest.py and is ready to run in an environment with pytest and network access to BASE_URL.

2) k6 run
- k6 was not executed in this runner (no k6 binary available here). k6 script exists at output/tests/qa_rate_limit_k6.js and should be run from an environment with k6 installed and network access to BASE_URL.

Artifacts created
- output/tests/qa_rate_limit_k6.js (k6 load script)
- output/tests/tests_retry_behavior_pytest.py (pytest suite)
- output/reports/qa_test_plan.md (QA test plan)
- output/reports/qa_rate_limit_retry_report.md (this file)

Blocking issues & required items from backend (Marcus / #ai-backend)
- Provide reachable staging BASE_URL and API_KEYS for test runs (env vars for k6 and pytest). Example: BASE_URL=https://staging.example.com API_KEYS=key-test-1,key-test-2
- Ensure test-only control endpoints are available and reachable from the test runner:
  - POST /test/rate_limit_mode?mode={soft|hard}
  - GET /test/retry/{502|always_503|...}
  - POST /test/idempotent_create
  - Test-only headers: X-Retry-Attempts, X-Retry-Timestamps, X-RateLimit-Mode
- Confirm Prometheus/Grafana telemetry endpoints and any dashboards to monitor during the canary (rate_limit, errors, retries, latency per API key).
- Provide a short rollback playbook (or pointer to runbook) and exact canary window dates.

Next steps for QA (blocked until above are provided)
- Re-run pytest in a runner with pytest installed and network access to BASE_URL, then attach junit XML to output/reports/pytest_results.xml and update this report with pass/fail details and failures (if any).
- Run k6 from a host with k6 installed using: BASE_URL=... API_KEYS=... k6 run output/tests/qa_rate_limit_k6.js and paste the k6 summary into this report.
- During soft canary (2 weeks): daily summary of errors, 95/99 latencies, rate-limit 429 counts per API key; immediate alert and rollback on any P1.

Contact
- QA lead: Dana (#ai-qa)

