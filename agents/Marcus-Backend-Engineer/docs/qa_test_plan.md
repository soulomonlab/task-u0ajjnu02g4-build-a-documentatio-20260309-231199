QA Test Plan: Rate Limit & Retry Behavior

Objective
- Verify per-API-key rate limiting (60 requests/minute, burst 10) and correct behavior in soft vs hard modes.
- Validate retry semantics: client retry rules, server idempotency support, jitter/backoff behavior, and observable retry headers.
- Provide acceptance criteria, schedule for a 2-week soft canary, telemetry checks, and rollback playbook.

Prerequisites
- Staging deployment URL (BASE_URL)
- Test API keys with controlled rate limits
- Test-only control endpoints exposed:
  - GET/POST /test/rate_limit_mode
  - GET /test/retry/{behavior}
  - GET /test/info
- Prometheus + Grafana access for SLO dashboards
- Test runner environments: k6 installed, Python pytest installed

Test Artifacts (created)
- output/tests/qa_rate_limit_k6.js — k6 script for sustained and burst scenarios
- output/tests/tests_retry_behavior_pytest.py — pytest cases for retry and idempotency

Environments & Variables
- k6: BASE_URL, API_KEYS (comma-separated)
- pytest: BASE_URL environment variable (defaults to http://localhost:8000)

Test Scenarios
1) Rate limit sustained throughput
   - Run k6 sustained scenario for 60s per API key, validate that per-key rate does not exceed 60rpm on average and that p95 latency < 200ms when not throttled.
   - Acceptance: Under soft mode, clients receive 429 with Retry-After header but requests still accepted (non-blocking analytics). Under hard mode, excess requests receive 429 and are dropped.

2) Burst behavior
   - Use burst scenario to send short high-rate bursts and verify that rate-limiter allows bursts up to 10 additional tokens.
   - Acceptance: Initial burst requests succeed (200) until burst tokens exhausted, then subsequent requests get 429.

3) Retry semantics & idempotency
   - Use pytest to exercise flaky endpoints and verify X-Retry-Attempts and X-Retry-TIMESTAMPS headers are present.
   - Validate idempotency for POST operations using Idempotency-Key header if endpoint available.

4) Backoff & jitter observational test
   - Ensure retry attempts include increasing delays between retries; inspect timestamps header for spacing.

5) Soft vs Hard mode behavior
   - Toggle /test/rate_limit_mode and verify system behavior for both modes.

Telemetry & Observability Checks
- Confirm Prometheus metrics exposed:
  - api_requests_total{status,api_key}
  - rate_limiter_throttled_requests_total{mode}
  - request_latency_seconds
- Confirm Grafana dashboards show alerts for sustained >80% of allocated request capacity per API key.

Acceptance Criteria
- Rate limiter enforces 60rpm +/- 5% per key, burst up to 10 tokens
- Soft mode: throttled requests produce metrics & 429+Retry-After but do not trigger circuit breakers
- Hard mode: excess requests are rejected and contribute to error budget
- Retry headers present and accurate; idempotency preserved for retried mutations

Schedule: 2-week Canary
- Week 0: Baseline tests in staging (run test suite)
- Week 1-2: Soft canary rollout to 10% of traffic (monitor metrics daily)
- Rollback if throttled_errors increase > 5% over baseline or p95 latency > 200ms for >3 consecutive 10m windows

Reporting
- QA will attach k6 summary, pytest XML, and logs into output/reports/qa_rate_limit_retry_report.md

